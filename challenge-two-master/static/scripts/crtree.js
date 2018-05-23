$(document).ready(function() {

    function task() {
        $.ajax({
            url: '/trash_counter',
            success: function(data) {
                $('#counter').html(data);
            },
            complete: function() {
                // Repeat in 5s
                setTimeout(task, 5000);
            }
        });
    }

    task();
});
