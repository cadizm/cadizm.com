
function onVrViewLoad() {
    var vrView = new VRView.Player('#vrview', {
        image: '//static/images/360/1f1a15e6-bff8-11e6-a89c-34363bc43fea.jpg',
        is_stereo: true
    });
}

window.addEventListener('load', onVrViewLoad);
