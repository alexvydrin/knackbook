
function advSearch() {
    var advSearchHolder = document.getElementById("div_adv_search"),
        flagSearchHolder = document.getElementById("flag_search"),
        ButtonSearchHolder = document.getElementById("adv_search");

    if(flagSearchHolder.value == "false"){
        ButtonSearchHolder.value = "—";
        ButtonSearchHolder.title = "Скрыть расширенный поиск";
        ButtonSearchHolder.blur();
        checkElements("true");
    } else {
        ButtonSearchHolder.value ="☰";
        ButtonSearchHolder.title = "Расширенный поиск";
        ButtonSearchHolder.blur();
        checkElements("false");
    }

    function checkElements(advanced_search){
        flagSearchHolder.value = advanced_search;
        if (advanced_search == "true") {
            advSearchHolder.classList.add('adv_search_block');
            advSearchHolder.classList.remove('adv_search_none');
        } else {
            advSearchHolder.classList.add('adv_search_none');
            advSearchHolder.classList.remove('adv_search_block');
        }

    }
}

