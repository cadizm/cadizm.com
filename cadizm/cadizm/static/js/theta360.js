
function openOverlay(imgId) {
    document.getElementById('overlay').style.width = '100%';

    var width = $(window).width().toString();
    var height = $(window).height().toString();

    var iframe = $('#iframe')[0];
    $(iframe).attr('src', ['https://theta360.com/s/', imgId, '?view=embed&width=', width, 'px&height=', height, 'px'].join(''));
    $(iframe).attr('style', ['width:', width, 'px;height:', height, 'px; max-width: 100%;'].join(''));

}

function closeOverlay() {
    document.getElementById('overlay').style.width = '0%';
}
