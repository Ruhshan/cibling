$(document).ready(function () {
    $("#id_date_of_birth").datepicker({
        language: 'en',
        maxDate: new Date(),
        dateFormat: 'yyyy-mm-dd'
    });
});