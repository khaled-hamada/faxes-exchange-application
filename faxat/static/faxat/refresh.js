
  window.onload=function(){

    if($('#ring').length > 0 &&  $('#ring_m').length > 0 ){
      document.getElementById("ring_m").play();
        // if (f() === 0){
      Push.create("فاكس / رسائل جديدة", {
            body: "لديك فاكس جديد "+"\n"+
                  "لديك رسائل جديدة",
            onClick: function () {
                window.focus();
                this.close();
            }
        });

      }
    else if($('#ring').length > 0){
      document.getElementById("ring").play();
        // if (f() === 0){
      Push.create("فاكس جديد", {
            body: "لديك فاكس جديد",
            onClick: function () {
                window.focus();
                this.close();
            }
        });

      }

      else if($('#ring_m').length > 0){
        document.getElementById("ring_m").play();
        // if (f() === 0){
          Push.create("رسائل جديدة", {
            body: "تم وصول رسائل جديدة",
            onClick: function () {
                window.focus();
                this.close();
            }
          });
        }

      // }


    }
    setTimeout(function() {
          //window.location.href = '/takt/';
          window.location.href = document.URL;
          // # min  *  # seconds per minute * #  milliseconds per second
        }, (1 * 60 * 1000));
