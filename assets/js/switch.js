var sizeSwitch = 27;
var switchHandle = $('#switch .handle');
var option1 = $('#option1');
var option2 = $('#option2');
var switchArea = $('#switch');

switchHandle.draggable({
    axis: 'x',
    containment: 'parent',
    stop: function () {
        conditionMove();
    }
});

option1.click(function () {
    option1.addClass('active');
    option2.removeClass('active');
    switchHandle.animate({
        left: 0
    }, 100);
});

option2.click(function () {
    option2.addClass('active');
    option1.removeClass('active');
    switchHandle.animate({
        left: sizeSwitch + 'px'
    }, 100);
});

switchArea.click(function () {
    conditionMoveSnap();
});

function conditionMove() {
    if (parseInt(switchHandle.css('left')) <= (sizeSwitch / 2)) {
        switchHandle.animate({
            left: 0
        }, 100);
        option1.addClass('active');
        option2.removeClass('active');
    } else {
        switchHandle.animate({
            left: sizeSwitch + 'px'
        }, 100);
        option2.addClass('active');
        option1.removeClass('active');
    }
}

function conditionMoveSnap() {
    if (parseInt(switchHandle.css('left')) == sizeSwitch) {
        switchHandle.animate({
            left: 0
        }, 100);
        option1.addClass('active');
        option2.removeClass('active');
    } else {
        switchHandle.animate({
            left: sizeSwitch + 'px'
        }, 100);
        option2.addClass('active');
        option1.removeClass('active');
    }
}
