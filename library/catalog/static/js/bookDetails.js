const timeToLiveMin = 10;
const starStorageKey = "bookDetailsRatingStar";
let ratingStars = document.querySelectorAll(".rating__control");

$(document).ready(function () {
  $(".toast").toast({ delay: 3000 });
  $(".toast").toast("show");

  let endpoint = document.getElementById("endpoint-list").getAttribute("url");
  let csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0]
    .value;

  $.ajax({
    method: "GET",
    url: endpoint,
    data: {
      csrfmiddlewaretoken: csrfmiddlewaretoken,
    },
    dataType: "json",
    success: fillCommentsList,
  });
});

ratingStars.forEach((ratingStar) => {
  ratingStar.addEventListener("click", function () {
    setWithExpiry(starStorageKey, parseInt(ratingStar.value), timeToLiveMin);
  });
});

function setWithExpiry(key, value, ttl) {
  let now = new Date();
  let item = {
    value: value,
    expiry: now.getTime() + ttl * 60000,
  };
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
  return item.value;
}

function saveStarRating(url) {
  let starValue = getWithExpiry(starStorageKey);
  if (starValue) {
    url = url + `${starValue}/`;
  }
  let request = new XMLHttpRequest();
  request.open("GET", url, true);
  request.send(null);
}

function addMouseEventsForComments() {
  let commentArea = document.querySelectorAll("#commentArea");
  commentArea.forEach((comment) => {
    comment.addEventListener("mouseover", function (event) {
      comment.querySelector("#commentButton").style.display = "block";
    });
    comment.addEventListener("mouseout", function (event) {
      comment.querySelector("#commentButton").style.display = "none";
    });
  });
}

function fillCommentsList(list) {
  let userId = document.getElementById("userId").getAttribute("value");
  let userRole = document.getElementById("userRole").getAttribute("value");

  const data = list.reviews;
  $("#commentList").empty();

  for (let i = 0; i < data.length; i++) {
    const buttonClass = `comment-delete-button-${i}`;
    const buttonClassAdmin = `comment-restore-button-${i}`;
    const userDeleteButton = `<a id="commentButton" style="float: right; width: 40px; display: none;"
                   class="btn btn-outline-danger ${buttonClass}">×</a>`;

    const adminRestoreButton = `<a id="commentButton" style="float: right; width: 80px; display: none;"
                   class="btn btn-outline-info ${buttonClassAdmin}">Restore</a>`;

    const date = new Date(data[i].fields.date).toLocaleDateString("en-US", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    });

    const regularUserComment =
      data[i].fields.status === "active" && `
          <div id="commentArea" >
          <div style="font-size: 15pt; background: white;" class="card-header">
                    ${data[i].fields.firstname} ${data[i].fields.lastname}
                    ${userId === data[i].fields.user && userDeleteButton ? userDeleteButton : ""}

             </div>
          <div class="card-body">
                        <blockquote class="blockquote mb-0">
                            <p style="font-size: 14pt">${data[i].fields.comment}</p>
                            <footer style="font-size: 10pt" class="blockquote-footer"><cite
                            title="Source Title">Published ${date}</cite></footer>
                </blockquote>
                     </div>
            </div>`;

    const adminComment = `
          <div id="commentArea" >
          <div style="font-size: 15pt; background: white;" class="card-header">
                    ${data[i].fields.firstname} ${data[i].fields.lastname}
                    ${
                      data[i].fields.status === "active"
                        ? userDeleteButton
                        : adminRestoreButton
                    }


             </div>
          <div class="card-body">
                        <blockquote class="blockquote mb-0">
                            <p style="font-size: 14pt">${data[i].fields.comment}</p>
                            <footer style="font-size: 10pt" class="blockquote-footer"><cite
                            title="Source Title">Published ${date}</cite></footer>
                </blockquote>
                     </div>
            </div>`;

    const content = userRole === "admin" ? adminComment : regularUserComment;

    if (content) {
      $("#commentList").append(content);
      if (userRole == "admin") {
      change_comment_status(`.${buttonClass}`,
      `/library/change_review_status/${data[i].fields.book}/${data[i].pk}/inactive/`,
      `/library/show_reviews/${data[i].fields.book}/`)
      change_comment_status(`.${buttonClassAdmin}`,
      `/library/change_review_status/${data[i].fields.book}/${data[i].pk}/active/`,
      `/library/show_reviews/${data[i].fields.book}/`)
      } else {
      change_comment_status(`.${buttonClass}`,
      `/library/change_review_status/${data[i].fields.book}/${data[i].pk}/inactive/`,
      `/library/show_reviews/${data[i].fields.book}/`)
      }
    }
    addMouseEventsForComments();
  }
}

addMouseEventsForComments();

function add_comment() {
  let textComment = document.getElementById("exampleFormControlTextarea1")
    .value;
  let endpoint = document
    .getElementById("endpoint-url-div")
    .getAttribute("url");
  let csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0]
    .value;
  document.getElementById("exampleFormControlTextarea1").value = "";
  $.ajax({
    method: "POST",
    url: endpoint,
    data: {
      csrfmiddlewaretoken: csrfmiddlewaretoken,
      "text-comment": textComment,
    },
    dataType: "json",
    success: fillCommentsList
  });
}

function change_comment_status(classname, url, getListURL) {
    let elementButton = document.querySelector(classname)
    if (elementButton){
    let csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0]
    .value;
    elementButton.onclick = function (){
                 $.ajax({
    method: "POST",
    url: url,
    data: {
      csrfmiddlewaretoken: csrfmiddlewaretoken
    },
    dataType: "json",
    complete:function(res){

    if (res.status === 200) {
        $.ajax({
        method:"GET",
        url: getListURL,
        data: {
            csrfmiddlewaretoken: csrfmiddlewaretoken
             },
    dataType: "json",
    success: fillCommentsList
        });
        }
    }
  });
  }
}
}

