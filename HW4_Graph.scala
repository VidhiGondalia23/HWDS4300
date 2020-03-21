import scala.collection.mutable.Map

class Graph {
  var nodes = Array[String]()
  var direction = scala.collection.mutable.Map[String, String]()
  var edgeList = scala.collection.mutable.Map[String,List[String]]()



  def addNode(str: String) {
    nodes += str
  }

  def addEdge(u: String, v: String): Unit = {
    direction += (u->v)
  }
  
  def adjacent(v: String): List[String] = {
    edgeList(v)
  }
  def shortestPath(u: String, v: String): List[String] = {
    
  }

}

Object Main extends App {
  Graph.addNode("a")
  Graph.addNode("b")
  Graph.addNode("c")
  Graph.addNode("d")
  Graph.addNode("e")
  Graph.addNode("e")
  Graph.addNode("f")
  
  println(Graph.nodes)
  
  Graph.addEdge("a", "b")
  Graph.addEdge("a", "c")
  Graph.addEdge("a", "d")
  Graph.addEdge("d", "e")
  Graph.addEdge("e", "f")
  println(Graph.direction)
  
  Graph.adjacent("a")
  Graph.adjacent("b")
  Graph.adjacent("d")
  Graph.adjacent("e")
  println(Graph.EdgeList) 
  
}
