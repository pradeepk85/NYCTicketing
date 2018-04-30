import org.apache.spark.sql.{SaveMode, SparkSession}
import org.apache.spark.sql.functions._

object NYCTickets {
  def main(args: Array[String]): Unit ={
    val spark = SparkSession.builder
      .appName("Spark Word Count")
      .getOrCreate()

//    val nyc2013 = spark.read.format("csv").option("header", "true").load("s3://mcsds-cs498/input/Parking_Violations_Issued_-_Fiscal_Year_2014__August_2013___June_2014_.csv, s3://mcsds-cs498/input/Parking_Violations_Issued_-_Fiscal_Year_2015.csv, s3://mcsds-cs498/input/Parking_Violations_Issued_-_Fiscal_Year_2016.csv, s3://mcsds-cs498/input/Parking_Violations_Issued_-_Fiscal_Year_2017.csv").cache()
    val nyc2013 = spark.read.format("csv").option("header", "true").load("s3://mcsds-cs498/input/*.csv")

    //Body Type
    val bodyType = nyc2013.groupBy("Vehicle Body Type").count().sort(desc("count"))
    val newSchemaVehicleBodyType = Seq("VehicleBodyType", "count")
    val bodyTypeWithNewSchema = bodyType.toDF(newSchemaVehicleBodyType: _*)
    val bodyTypeWithoutNull = bodyTypeWithNewSchema.filter("VehicleBodyType is not null and VehicleBodyType != ''")
    bodyTypeWithoutNull.coalesce(1).write.mode(SaveMode.Append).format("csv").option("header","false").save("s3://mcsds-cs498/output/bodytype/")


    //Plate Type
    val plateType = nyc2013.groupBy("Plate Type").count().sort(desc("count"))
    val newSchemaPlateType = Seq("PlateType", "count")
    val plateTypeWithNewSchema = plateType.toDF(newSchemaPlateType: _*)
    val plateTypeWithoutNull = plateTypeWithNewSchema.filter("PlateType is not null and PlateType != ''")
    plateTypeWithoutNull.coalesce(1).write.mode(SaveMode.Append).format("csv").option("header","false").save("s3://mcsds-cs498/output/platetype/")


    //County Type
    val violationCounty = nyc2013.groupBy("Violation County").count().sort(desc("count"))
    val newSchemaVilolationCounty = Seq("ViolationCounty", "count")
    val violationCountyWithNewSchema = violationCounty.toDF(newSchemaVilolationCounty: _*)
    val violationCountyWithoutNull = violationCountyWithNewSchema.filter("ViolationCounty is not null and ViolationCounty != ''")
    violationCountyWithoutNull.coalesce(1).write.mode(SaveMode.Append).format("csv").option("header","false").save("s3://mcsds-cs498/output/countytype/")

    //Violation Time
    def show(x: Option[String]) = x match {
      case Some(s) => s
      case None => "?"
    }


    def cast(number: Any): Float = number match {
      case n: Float => n.toFloat
      case x => 0
    }

    def hourFormat(inputString: String): Option[Float] = {
      val input = Option(inputString).getOrElse(return None)
      if (input.isEmpty) return None else {
        val time1 = input.substring(0, 2)
        val time = if (time1.forall(_.isDigit)) Some(time1.toFloat) else None
        val timeAMPM = if (input.length > 4) Some(input.substring(4, 5)) else None

        if (show(timeAMPM) == "P") Some(cast(time) % 12 + 12.toFloat) else time
      }
    }

    val hourFormatUdf = udf(hourFormat _)
    val ticketByTimeHour = nyc2013.select(hourFormatUdf(nyc2013("Violation Time")) as "hour")
    val violationTime = ticketByTimeHour.groupBy("hour").count().sort(desc("count"))
    val newSchemaViolationTime = Seq("hour","count")
    val violationTimeWithNewSchema = violationTime.toDF(newSchemaViolationTime: _*)
    val violationTimeWithoutNull = violationTimeWithNewSchema.filter("hour is not null")
    violationTimeWithoutNull.coalesce(1).write.mode(SaveMode.Append).format("csv").option("header","false").save("s3://mcsds-cs498/output/violationtype/")



    spark.stop()

  }
}
