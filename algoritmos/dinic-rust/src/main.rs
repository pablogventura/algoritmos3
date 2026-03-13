//! # Dinic — flujo máximo
//!
//! Entrada: líneas `x y cap` por stdin. Fuente = 0, sumidero = 1.
//! Con la feature `parallel` se paraleliza el BFS por niveles (rayon). Requiere Rust 1.80+.
//!
//! Estructura del módulo:
//! - Tipos: `Edge`, `Vertex`, `Network`, `DinicState`
//! - Red: construcción (`add_edge`, `set_source_sink`)
//! - Niveles: `bfs_levels` (BFS en la red residual)
//! - Blocking flow: `dfs_blocking`, `blocking_flow`, `run_dinic`
//! - I/O: `main` (lectura stdin, salida del valor del flujo)

use std::collections::VecDeque;
use std::io::{self, BufRead, BufReader, Write};

#[cfg(feature = "parallel")]
use rayon::prelude::*;

// -----------------------------------------------------------------------------
// Tipos de la red
// -----------------------------------------------------------------------------

type VertexId = usize;
type EdgeId = usize;

const SOURCE_LABEL: u32 = 0;
const SINK_LABEL: u32 = 1;
const LEVEL_UNREACHABLE: u32 = u32::MAX;

#[derive(Clone)]
struct Edge {
    from: VertexId,
    to: VertexId,
    capacity: u32,
    flow: u32,
}

#[derive(Clone)]
struct Vertex {
    label: u32,
    forward_edges: Vec<EdgeId>,
    backward_edges: Vec<EdgeId>,
}

struct Network {
    vertices: Vec<Vertex>,
    edges: Vec<Edge>,
    label_to_idx: std::collections::HashMap<u32, VertexId>,
    source: VertexId,
    sink: VertexId,
}

/// Estado para BFS de niveles y DFS de blocking flow.
struct DinicState {
    level: Vec<u32>,
    /// Índice de la siguiente arista a probar por vértice (current arc).
    current_forward: Vec<usize>,
    current_backward: Vec<usize>,
    queue: VecDeque<VertexId>,
    #[cfg(feature = "parallel")]
    level_a: Vec<VertexId>,
    #[cfg(feature = "parallel")]
    level_b: Vec<VertexId>,
}

// -----------------------------------------------------------------------------
// Construcción de la red
// -----------------------------------------------------------------------------

impl Network {
    fn new() -> Self {
        Network {
            vertices: Vec::new(),
            edges: Vec::new(),
            label_to_idx: std::collections::HashMap::new(),
            source: 0,
            sink: 0,
        }
    }

    fn get_or_create_vertex(&mut self, label: u32) -> VertexId {
        if let Some(&idx) = self.label_to_idx.get(&label) {
            return idx;
        }
        let idx = self.vertices.len();
        self.vertices.push(Vertex {
            label,
            forward_edges: Vec::new(),
            backward_edges: Vec::new(),
        });
        self.label_to_idx.insert(label, idx);
        idx
    }

    fn add_edge(&mut self, x: u32, y: u32, cap: u32) {
        let from = self.get_or_create_vertex(x);
        let to = self.get_or_create_vertex(y);
        let edge_id = self.edges.len();
        self.edges.push(Edge {
            from,
            to,
            capacity: cap,
            flow: 0,
        });
        self.vertices[from].forward_edges.push(edge_id);
        self.vertices[to].backward_edges.push(edge_id);
    }

    fn set_source_sink(&mut self) {
        self.source = self.label_to_idx[&SOURCE_LABEL];
        self.sink = self.label_to_idx[&SINK_LABEL];
    }

    fn num_vertices(&self) -> usize {
        self.vertices.len()
    }

    // -------------------------------------------------------------------------
    // BFS de niveles (red residual)
    // -------------------------------------------------------------------------

    /// Asigna nivel (distancia) desde source. Devuelve true si el sumidero es alcanzable.
    #[cfg(not(feature = "parallel"))]
    fn bfs_levels(&mut self, state: &mut DinicState) -> bool {
        state.level.fill(LEVEL_UNREACHABLE);
        state.level[self.source] = 0;
        state.queue.clear();
        state.queue.push_back(self.source);

        while let Some(v) = state.queue.pop_front() {
            let lv = state.level[v];
            for &eid in &self.vertices[v].forward_edges {
                let e = &self.edges[eid];
                let res = e.capacity.saturating_sub(e.flow);
                if res > 0 && state.level[e.to] == LEVEL_UNREACHABLE {
                    state.level[e.to] = lv + 1;
                    state.queue.push_back(e.to);
                }
            }
            for &eid in &self.vertices[v].backward_edges {
                let e = &self.edges[eid];
                if e.flow > 0 && state.level[e.from] == LEVEL_UNREACHABLE {
                    state.level[e.from] = lv + 1;
                    state.queue.push_back(e.from);
                }
            }
        }
        state.level[self.sink] != LEVEL_UNREACHABLE
    }

    #[cfg(feature = "parallel")]
    fn bfs_levels(&mut self, state: &mut DinicState) -> bool {
        state.level.fill(LEVEL_UNREACHABLE);
        state.level[self.source] = 0;
        let (current, next) = (&mut state.level_a, &mut state.level_b);
        current.clear();
        next.clear();
        current.push(self.source);

        let vertices = &self.vertices;
        let edges = &self.edges;
        let sink = self.sink;

        while !current.is_empty() {
            let levels_cur: Vec<u32> = current.iter().map(|&v| state.level[v]).collect();
            let discoveries: Vec<(VertexId, u32)> = current
                .par_iter()
                .enumerate()
                .flat_map(|(i, &v)| {
                    let lv = levels_cur[i];
                    let mut list = Vec::new();
                    for &eid in &vertices[v].forward_edges {
                        let e = &edges[eid];
                        if e.capacity.saturating_sub(e.flow) > 0 {
                            list.push((e.to, lv + 1));
                        }
                    }
                    for &eid in &vertices[v].backward_edges {
                        let e = &edges[eid];
                        if e.flow > 0 {
                            list.push((e.from, lv + 1));
                        }
                    }
                    list
                })
                .collect();

            for (w, lw) in discoveries {
                if state.level[w] == LEVEL_UNREACHABLE {
                    state.level[w] = lw;
                    next.push(w);
                }
            }
            if state.level[sink] != LEVEL_UNREACHABLE {
                return true;
            }
            if next.is_empty() {
                return false;
            }
            std::mem::swap(current, next);
            next.clear();
        }
        false
    }

    // -------------------------------------------------------------------------
    // Flujo bloqueante (DFS con current arc)
    // -------------------------------------------------------------------------

    /// DFS desde v hacia el sumidero en el grafo de niveles. Current arc en `state` evita reescanear aristas.
    fn dfs_blocking(
        &mut self,
        v: VertexId,
        flow_in: u64,
        state: &mut DinicState,
        path: &mut Vec<(EdgeId, bool)>,
    ) -> u64 {
        if v == self.sink {
            return flow_in;
        }
        let lv = state.level[v];

        // Forward edges (no guardar referencia a self.vertices para permitir borrow mut en dfs_blocking)
        while state.current_forward[v] < self.vertices[v].forward_edges.len() {
            let eid = self.vertices[v].forward_edges[state.current_forward[v]];
            state.current_forward[v] += 1;
            let e = &self.edges[eid];
            let w = e.to;
            if state.level[w] != lv + 1 {
                continue;
            }
            let res = e.capacity.saturating_sub(e.flow) as u64;
            if res == 0 {
                continue;
            }
            let send = flow_in.min(res);
            path.push((eid, true));
            let got = self.dfs_blocking(w, send, state, path);
            path.pop();
            if got > 0 {
                self.edges[eid].flow += got as u32;
                return got;
            }
        }

        // Backward edges
        while state.current_backward[v] < self.vertices[v].backward_edges.len() {
            let eid = self.vertices[v].backward_edges[state.current_backward[v]];
            state.current_backward[v] += 1;
            let e = &self.edges[eid];
            let w = e.from;
            if state.level[w] != lv + 1 {
                continue;
            }
            if e.flow == 0 {
                continue;
            }
            let send = flow_in.min(e.flow as u64);
            path.push((eid, false));
            let got = self.dfs_blocking(w, send, state, path);
            path.pop();
            if got > 0 {
                self.edges[eid].flow -= got as u32;
                return got;
            }
        }
        0
    }

    /// Una ronda de blocking flow: repetir DFS hasta agotar. Devuelve flujo total enviado.
    fn blocking_flow(&mut self, state: &mut DinicState) -> u64 {
        state.current_forward.fill(0);
        state.current_backward.fill(0);
        let mut total = 0u64;
        let mut path = Vec::new();
        loop {
            let f = self.dfs_blocking(self.source, u64::MAX, state, &mut path);
            if f == 0 {
                break;
            }
            total += f;
        }
        total
    }

    fn run_dinic(&mut self, state: &mut DinicState) -> u64 {
        let mut max_flow = 0u64;
        while self.bfs_levels(state) {
            max_flow += self.blocking_flow(state);
        }
        max_flow
    }
}

// -----------------------------------------------------------------------------
// Entrada/salida
// -----------------------------------------------------------------------------

fn main() -> io::Result<()> {
    let reader = BufReader::with_capacity(256 * 1024, io::stdin().lock());
    let mut network = Network::new();

    for line in reader.lines() {
        let line = line?;
        let line = line.trim();
        if line.is_empty() {
            continue;
        }
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() != 3 {
            continue;
        }
        let x: u32 = match parts[0].parse() {
            Ok(n) => n,
            _ => continue,
        };
        let y: u32 = match parts[1].parse() {
            Ok(n) => n,
            _ => continue,
        };
        let cap: u32 = match parts[2].parse() {
            Ok(n) => n,
            _ => continue,
        };
        network.add_edge(x, y, cap);
    }

    network.set_source_sink();
    let n = network.num_vertices();

    let mut state = DinicState {
        level: vec![0; n],
        current_forward: vec![0; n],
        current_backward: vec![0; n],
        queue: VecDeque::with_capacity(n),
        #[cfg(feature = "parallel")]
        level_a: Vec::with_capacity(n),
        #[cfg(feature = "parallel")]
        level_b: Vec::with_capacity(n),
    };

    let max_flow = network.run_dinic(&mut state);

    let stdout = io::stdout();
    let mut out = stdout.lock();
    writeln!(out, "Valor del flujo maximal : {}", max_flow)?;
    Ok(())
}
