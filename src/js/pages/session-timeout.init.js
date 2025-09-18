/*
Template Name: 
Author: Themesdesign
Website: https://themesdesign.in/
Contact: themesdesign.in@gmail.com
File: Session Timeout Js File
*/

$.sessionTimeout({
    keepAliveUrl: '/notifications/starter-page',
    logoutButton: 'Logout',
    logoutUrl: '/account/logout/',
    redirUrl: '/notifications/authentication/lock-screen',
    warnAfter: 3000,
    redirAfter: 30000,
    countdownMessage: 'Redirecting in {timer} seconds.'
});

$('#session-timeout-dialog [data-dismiss=modal]').attr("data-bs-dismiss", "modal");
$('#session-timeout-dialog [data-dismiss=modal]').removeAttr("data-dismiss");