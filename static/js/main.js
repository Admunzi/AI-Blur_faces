$( document ).ready(function() {
    // disable form submit on click on button and get value from input with name "list_images"
    $( "#form_download" ).submit(function( event ) {
        event.preventDefault();
        // We will get array value from list_images input and transform to array, it have this sintax:
        var list_images = $( "input[name='list_images']" ).val();

        // We will transform string to array
        list_images = list_images.replace(/'/g, '"');
        list_images = JSON.parse(list_images);

        // call function to download images
        downloadImages(list_images);
    });

    $('form input').change(function () {
        $('form p').text(this.files.length + " file(s) selected");
      });
      
    // function to download images
    function downloadImages(list_images) {
        list_images.forEach(function(image) {
            console.log(image);
            console.log( typeof image);
            var link = document.createElement("a");
            link.download = image;
            link.href = "/static/uploads/" + image;
            link.click();
        })
    }

});

