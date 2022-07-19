window.addEventListener('load', function() {
    function milliCentsInputToValue(s) {
        return Math.round(parseFloat(s) * 100000);
    };
    function milliCentsValueToInput(v) {
        return (v / 100000.0).toFixed(2);
    };
    function setupMilliCentsWidget(hidden) {
        var base_id = hidden.id;
        var input_id = base_id + '_input';
        var text_id = base_id + '_text';

        var input = document.getElementById(input_id);
        var text = document.getElementById(text_id);
        text.innerText = hidden.value;

        input.value = milliCentsValueToInput(hidden.value);
        input.addEventListener('input', function (e) {
            var value = milliCentsInputToValue(e.target.value);
            hidden.value = value;
            text.innerText = value;
        });
    };
    var hiddens = document.getElementsByClassName('price-milli-cents-hidden');
    for (let i = 0; i < hiddens.length; i++) {
        const hidden = hiddens[i];
        setupMilliCentsWidget(hidden);
    }
});
