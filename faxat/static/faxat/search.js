$(document).ready(function(){

      $("input").hide();
    $("#search_list").change(function(){

        $(this).find("option:selected").each(function(){
              $("#sbt").show();
            var optionValue = $(this).attr("value");
            if(optionValue == 1){
                $("input").hide();
                $("label").hide();

                $("#title").show();
                // $("option[selected='false']", "#search_list").each(fuction(){
                //   $(this).hide();
                // });
              //  $("otion:unselected").hide();
            }
            else if(optionValue == 2){
                $("input").hide();
                $("#date").show();
            }
            else if(optionValue == 3){
                $("input").hide();
                $("#sader_edara").show();
            }
            else if(optionValue == 4){
                $("input").hide();
                $("#sader").show();
            }
            else if(optionValue == 5){
                $("input").hide();
                $("#approved_by").show();
            }
            else if(optionValue == 6){
                $("input").hide();
                $("#date_period_1").show();
                $("#date_period_2").show();
            }
            else if(optionValue == 7){
                $("input").hide();
                $("#dept_name").show();

            }
            else if(optionValue == 8){
                $("input").hide();
                $("#not_seen").show();

            }
            else if(optionValue == 9){
                $("input").hide();
                $("#all_faxes").val("all_faxes");

            }
            $("#sbt").show();


        });
    }).change();
});
