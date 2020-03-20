package breeze.plot
import breeze.plot._

//homework
object Binary extends App{
  def toBinary(x:Int, bits: Int):String = {
    if(x==0)
      "0"*bits
    else if (x==1)
      "0"* (bits-1)+"1"
    else toBinary(x/2, bits-1) + (x%2).toString
  }


  // can replace below thing to -------> Int=b.count(_=='1')
  def weight(b:String):Int = b.count((x:Char) => x == '1')
  val bin = toBinary(37, 8)
  print(weight(bin))


  val xs = Range(0,1025)
  val ys = xs.map(x=>weight(toBinary(x,8)))
  print(ys)


  val fig = Figure()
  val plt = fig.subplot(0)
  plt += plot(xs, ys)
  fig.refresh()

}

