/*
Template Name: 
Author: Themesdesign
Website: https://themesdesign.in/
Contact: themesdesign.in@gmail.com
File: two step verification Init Js File
*/


// move next
function moveToNext(elem, count) {
    if (elem.value.length > 0) {
        $("#digit" + count + "-input").focus();
    }
}