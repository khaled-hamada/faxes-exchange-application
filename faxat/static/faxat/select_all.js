function toggle(source, list_name) {
  checkboxes = $("input[name='send_depts']");
  for(var i=0, n = checkboxes.length; i<n; i++) {
    checkboxes[i].checked = source.checked;
  }
}


function toggle_reply(source, list_name) {
  checkboxes = $("input[name='reply_depts']");
  for(var i=0, n = checkboxes.length; i<n; i++) {
    checkboxes[i].checked = source.checked;
  }
}


// Listen for click on toggle checkbox
// $('#select-all').click(function(event) {
//     if(this.checked) {
//         // Iterate each checkbox
//         $(':checkbox').each(function() {
//             this.checked = true;
//         });
//     } else {
//         $(':checkbox').each(function() {
//             this.checked = false;
//         });
//     }
// });
