import scala.collection.mutable.Map



class RedisR(val key: String, val value: String){
  val supers = scala.collection.mutable.Map[String, String]()

  def get(key: String):String = {
    if(supers.contains(key)) supers(key) else ""
  }

  def set(key: String, value: String): Unit = {
    supers += (key -> value)
  }


//  def lrange(key: String, start: Int, stop: Int): List[String]


}

object RedisR {

  val supers = scala.collection.mutable.Map("Bruce Wayne" -> "Batman")

  def set(key: String, value: String): Unit = {
    val name = scala.collection.mutable.Map(key -> value)
  }

  def get(key: String):String = {
    if(supers.contains(key)) supers(key) else ""
  }

  def lpush(key: String, value: String): Unit ={
    supers += (key -> value)
  }

  def lpop(key: String): Unit ={
    supers - key
  }

  def llen(key: String): Int = {
    supers.size
  }

  def rpush(key: String, value: String)= {
    var su = key -> value
    (supers ++: Seq(su)).toMap
  }

  def rpop(key: String): Unit={
    supers .-(key)
  }

  def flushall(): Unit = {
    supers.clear()
  }
//Map is unordered which makes it difficult to show a range of map elements based on index (start and end)
//  def lrange(key: String, start: Int, stop: Int): List[String] = {
//    key.slice(start, stop).toList
//  }


}

object Main1 extends App {
  println(RedisR.set("Clarke Kent", "Superman"))
  println(RedisR.supers)
  println(RedisR.get("Bruce Wayne"))
  println(RedisR.lpush("Clarke Kent", "Superman"))
  println(RedisR.supers)
  println(RedisR.rpush("Tony Stark", "Iron Man"))
  println(RedisR.supers)
  println(RedisR.lpop("Clarke Kent"))
  println(RedisR.supers)
  println(RedisR.rpop("Tony Stark"))
  println(RedisR.llen("Tony Stark"))

//  println(RedisR.supers)
}
--------------------==========================LISTBUFFER====================--------------------
import scala.collection.mutable.{Buffer, ListBuffer}


class Redis (var superhero:ListBuffer[(String, String)]){


}

object Redis {
  var LB = ("", "")
  var supers = ListBuffer(("Clarke", "Superman"))

  //  def lrange(key: String, start: Int, stop: Int): List[String]
  //  def flushall()

  def set(key: String, value:String) {
    var newlb = LB.copy (_1 = key, _2 = value)
    return newlb
    println(newlb)
  }

//  def get(key: String):Boolean = {
//  }

  def rpush(key:String, value:String){
    val valpair = (key, value)
    supers.+=(valpair)
  }


  def lpush(key:String, value:String){
    Tuple2(key, value) +=: supers
  }

  def llen(): Int = {
    supers.length
  }

  def rpop():Unit = {
    supers.remove(llen()-1)
  }

  def lpop():Unit = {
    supers.remove(0)
    return supers
  }

  def lrange(key: ListBuffer[(String, String)], start: Int, stop:Int):ListBuffer[(String, String)] ={
    key.slice(start, stop)
  }

  def flushall(): Unit ={
    supers.clear()
  }

}

object Main extends App {

  var supers = ListBuffer(("Clarke", "Superman"))
  Redis.set("Tony", "IronMan")
  //print(Redis.LB)

  println(Redis.set("Tony", "IronMan"))
  println(Redis.rpush("Bruce", "Batman"))
  println(Redis.supers)
  println(Redis.lpush("Peter", "Spiderman"))
  println(Redis.supers)
  println(Redis.lpop())
  println(Redis.supers)
  Redis.rpush("Arthur", "Aquaman")
  println(Redis.supers)
  println(Redis.llen())
  Redis.rpop()
  println(Redis.supers)

  println(Redis.lrange(supers,0, 2 ))

}
