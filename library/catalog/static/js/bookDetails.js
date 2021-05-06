const timeToLiveMin = 10;
const starStorageKey = 'bookDetailsRatingStar';
let ratingStars = document.querySelectorAll('.rating__control');

ratingStars.forEach(ratingStar => {
    ratingStar.addEventListener('click', function () {
        setWithExpiry(starStorageKey, parseInt(ratingStar.value), timeToLiveMin);
    })
})

function setWithExpiry(key, value, ttl) {
    let now = new Date()
    let item = {
        value: value,
        expiry: now.getTime() + ttl * 60000,
    }
    localStorage.setItem(key, JSON.stringify(item));
}

function getWithExpiry(key) {
    const itemStr = localStorage.getItem(key);
    if (!itemStr) {
        return null;
    }
    let item = JSON.parse(itemStr);
    let now = new Date();
    if (now.getTime() > item.expiry) {
        localStorage.removeItem(key);
        return null;
    }
    return item.value
}

function saveStarRating(url) {
    let starValue = getWithExpiry(starStorageKey);
    if (!starValue) {
        location.replace(url);
    } else {
        location.replace(url + `${starValue}/`);
    }
}
