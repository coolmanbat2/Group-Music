/**
 * Returns a CSRF Token cookie for the current running app this function is used on.
 * 
 * Usage: GetCookie() returns a CSRF Token
 * @param {string} name 
 */
function GetCookie() {
    let name = 'csrftoken';
    let cookieValue = null;
   
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Look for the cookie defined in the variable 'name'.
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export default GetCookie;