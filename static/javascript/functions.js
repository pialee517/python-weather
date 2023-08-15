const search = document.getElementById("txt_search");
const clear = document.getElementById('btn_clear');
const submit = document.getElementById('btn_submit');
const form = document.getElementById('search_form');
const error = document.getElementById('error_msg');

clear.addEventListener('click', clearSearchbar);
submit.addEventListener('click', checkValue);

function clearSearchbar() {
       search.value = '';
}

function checkValue(){
    console.log(search.value);
    if (search.value === 'undefined' || search.value.trim() === ''){
        search.placeholder = 'Error: Please check out your input';
        search.classList.add('error');
    }else{
        search.classList.remove('error');
        search.placeholder = 'City';
        form.submit();
    }
}