// Setting content of page upto certain limit for better display
function setContentLength(){
    contentElementList = document.getElementsByClassName('page_content');
    for(let content of contentElementList){
        page_element = content.parentNode
        load_value = content.innerHTML;

        // Setting additional height other than page content height + add_on for page height in different screen size
        if(content.innerHTML.length > 220){
            content.innerHTML = `${load_value.slice(0, 217)}...`;
        }
        const mediaQuery400 = window.matchMedia('(max-width: 400px)'); // Ensuring screen size
        const mediaQuery800 = window.matchMedia('(max-width: 800px)'); // Ensuring screen size
        add_on = getAddOn(mediaQuery400, mediaQuery800)
        page_element.style.maxHeight = '1000px';
        page_element.style.height =  (content.offsetHeight + add_on) + 'px';
    }
}
window.addEventListener('load', setContentLength)


// Event handler when edit button is clicked
function editButton(event){
    event.stopPropagation();
    let permission = window.confirm("Do you want to modify this task?")
    if(permission){
        let edit_page_url = event.target.parentNode.dataset.codeEdit;
        window.location.href = edit_page_url
    }

}


// Event handler when delete button is clicked
function deleteButton(event){
    event.stopPropagation();
    let permission = confirm("Are you sure to delete this task?")
    if(permission){
        let delete_url = event.target.parentNode.dataset.codeDelete;
        window.location.href = delete_url

    }
}


// expand a page div of task based on different media screens
function expandPage(event, original_data){
    const mediaQuery400 = window.matchMedia('(max-width: 400px)'); // Ensuring screen size
    const mediaQuery800 = window.matchMedia('(max-width: 800px)'); // Ensuring screen size
    page_element = event.target.parentNode;
    page_container_element = document.getElementsByClassName('page_container')[0];
    page_content_element = page_element.getElementsByClassName('page_content')[0];

    current_data = page_content_element.innerHTML;
    // Expand sliced text of page_content and modify style of elements based on it
    if (current_data.length <= 220 && original_data.length > 220){
        if(mediaQuery400.matches && mediaQuery800.matches){
            page_container_element.style.gridTemplateColumns = '1fr';

            
            page_content_element.style.wordWrap = 'break-word';
            page_content_element.innerHTML = original_data;
        }
        else {
            page_container_element.style.gridTemplateColumns = 'auto';
            page_element.style.width = 'device-width';
            
            page_content_element.style.wordWrap = 'break-word';
            page_content_element.innerHTML = original_data;
        }
    }
    // Slice text of page_content and modify style of elements based on it
    else if (current_data.length > 220 && original_data.length > 220) {
        if (mediaQuery400.matches || mediaQuery800.matches){
            page_container_element.style.gridTemplateColumns = '1fr';
        }
        else {
            page_container_element.style.gridTemplateColumns = 'auto auto';
        }
        page_element.removeAttribute('style');
        page_content_element.removeAttribute('style');

        // Reset Page
        setContentLength();
    }
    // Setting additional height other than page content height + add_on for page height in different screen size
    add_on = getAddOn(mediaQuery400, mediaQuery800);
    page_element.style.maxHeight = '1000px';
    page_element.style.height =  (page_content_element.offsetHeight + add_on) + 'px';

    // Scroll to selected page
    page_element.scrollIntoView({ behavior: "smooth" });
}


// Setting additional height other than page content height + add_on for page height in different screen size
function getAddOn(_400, _800){
        if (_400.matches){
            add_on = 100
        }
        else if (_800.matches){
            add_on = 100
        }
        else {
            add_on = 100
        }
        return add_on
}
