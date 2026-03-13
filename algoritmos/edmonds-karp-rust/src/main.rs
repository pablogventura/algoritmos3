//! Edmonds-Karp para flujo máximo. Port de la implementación en C.
//! Entrada: líneas "x y cap" por stdin. Fuente = 0, sumidero = 1.

use std::collections::VecDeque;
use std::io::{self, BufRead, Write};

type VertexId = usize;
type EdgeId = usize;

const SOURCE_LABEL: u32 = 0;
const SINK_LABEL: u32 = 1;

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

/// Información auxiliar para BFS y aumento de flujo (equivalente a info_s en C).
struct BfsInfo {
    in_cut: Vec<bool>,
    ancestor: Vec<Option<VertexId>>,
    forward_edge: Vec<bool>,
    accumulated_flow: Vec<u64>,
}

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

    /// BFS desde source hacia sink. Devuelve true si hay camino aumentante.
    /// Rellena BfsInfo: cut, ancestor, forward_edge, accumulated_flow.
    fn find_shortest_augmenting_path(&mut self, info: &mut BfsInfo) -> bool {
        let n = self.num_vertices();
        info.in_cut.fill(false);
        for i in 0..n {
            info.ancestor[i] = None;
            info.accumulated_flow[i] = u64::MAX;
        }

        let mut queue = VecDeque::new();
        queue.push_back(self.source);
        info.in_cut[self.source] = true;
        info.accumulated_flow[self.source] = u64::MAX;

        while let Some(v) = queue.pop_front() {
            if v == self.sink {
                return true;
            }
            // Forward: aristas salientes con capacidad residual
            for &eid in &self.vertices[v].forward_edges {
                let edge = &self.edges[eid];
                let w = edge.to;
                let residual = edge.capacity.saturating_sub(edge.flow) as u64;
                if residual > 0 && !info.in_cut[w] {
                    info.in_cut[w] = true;
                    info.ancestor[w] = Some(v);
                    info.forward_edge[w] = true;
                    info.accumulated_flow[w] = info.accumulated_flow[v]
                        .min(residual);
                    queue.push_back(w);
                }
            }
            // Backward: aristas entrantes con flujo > 0
            for &eid in &self.vertices[v].backward_edges {
                let edge = &self.edges[eid];
                let w = edge.from;
                if edge.flow > 0 && !info.in_cut[w] {
                    info.in_cut[w] = true;
                    info.ancestor[w] = Some(v);
                    info.forward_edge[w] = false;
                    info.accumulated_flow[w] = info.accumulated_flow[v]
                        .min(edge.flow as u64);
                    queue.push_back(w);
                }
            }
        }
        false
    }

    /// Aumenta el flujo a lo largo del camino encontrado por BFS. Devuelve epsilon.
    fn increase_flow(&mut self, info: &BfsInfo, max_flow: &mut u64) -> u32 {
        let epsilon = info.accumulated_flow[self.sink] as u32;
        *max_flow += epsilon as u64;

        let mut v = self.sink;
        while v != self.source {
            let u = info.ancestor[v].unwrap();
            if info.forward_edge[v] {
                // Arista u -> v (forward): aumentar flujo en la arista u->v
                let eid = self.vertices[v].backward_edges.iter().copied().find(|&eid| self.edges[eid].from == u).unwrap();
                self.edges[eid].flow += epsilon;
            } else {
                // Arista v -> u (backward): disminuir flujo en la arista v->u
                let eid = self.vertices[v].forward_edges.iter().copied().find(|&eid| self.edges[eid].to == u).unwrap();
                self.edges[eid].flow -= epsilon;
            }
            v = u;
        }
        epsilon
    }
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let mut network = Network::new();

    // Leer red desde stdin: "x y cap"
    for line in stdin.lock().lines() {
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

    let mut info = BfsInfo {
        in_cut: vec![false; n],
        ancestor: vec![None; n],
        forward_edge: vec![false; n],
        accumulated_flow: vec![0; n],
    };

    let mut max_flow: u64 = 0;

    while network.find_shortest_augmenting_path(&mut info) {
        network.increase_flow(&info, &mut max_flow);
        // Opcional: imprimir cada camino (como en C). Para tests con -v 0 no hace falta.
        // Aquí no imprimimos cada camino para que la salida sea compatible con la última línea "Valor del flujo maximal"
    }

    // Imprimir corte minimal y valor del flujo (como la versión C)
    let stdout = io::stdout();
    let mut out = stdout.lock();
    write!(out, "Corte Minimal: S = {{")?;
    let mut first = true;
    for (i, &in_s) in info.in_cut.iter().enumerate() {
        if in_s {
            if !first {
                write!(out, ", ")?;
            }
            let label = network.vertices[i].label;
            if label == SOURCE_LABEL {
                write!(out, "s")?;
            } else if label == SINK_LABEL {
                write!(out, "t")?;
            } else {
                write!(out, "{}", label)?;
            }
            first = false;
        }
    }
    writeln!(out, "}}")?;
    writeln!(out, "Capacidad: {}", max_flow)?;
    writeln!(out, "Valor del flujo maximal : {}", max_flow)?;

    Ok(())
}
