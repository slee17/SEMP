$(function() {

	// Change the on_sale status of a shift on submit
	$('#shift-sale-form').on('submit', function(event){
		event.preventDefault(); // Prevent the default browser behavior for a form submission.
		console.log("Form submitted.") // Sanity check.
		create_sale();
	})

    // AJAX for creating shift sales
    function create_sale() {
        // Submit form data to the create_sale/ endpoint, and wait for either _success_ or _error_.
        console.log("Create shift is working!") // sanity check
        $.ajax({
            url: "create_sale/", // the endpoint
            type: "POST", // http method
            data: { the_shift: $('#shift-on-sale').val() }, // data sent with the post request

            // handle a successful response
            success: function(json) {
                $('#shift-on-sale').val(''); // Remove the value from the input.
                console.log(json); // Log the returned json to the console.
                $("#talk").prepend("<li><strong>"+json.shift_id+"</strong> - <em> "
                    +json.on_sale+"</em> - <span> "+json.created+"</span> - <a id='delete-post-"
                    +json.postpk+"'>delete me</a></li>");
                console.log("success"); // another sanity check
            },
            // handle a non-successful response
            error: function(xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>An error
                occurred: "+errmsg+" <a href='#' class='close'>&times;</a></div>"); // Add the error to the DOM.
                console.log(xhr.status+": "+xhr.responseText); // Provide more info about the error to the console.
            }
        });
    };

    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});