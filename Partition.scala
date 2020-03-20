object Partition {
  def moved(records:Int, startN:Int, endN:Int): Double = {
    var fromRecords = records.toDouble/startN
    var toRecords = records.toDouble/endN

    var exact = fromRecords - toRecords

    return exact


  }

  print("Total records moved would be " + moved(1000000,100, 107)*100 )
}
