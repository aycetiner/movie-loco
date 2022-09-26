//GOOGLE MAPS API

let map;
let marker;
let geocoder;
let responseDiv;
let response;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 8,
    center: { lat: 41.881, lng: -87.623177 },
    mapTypeControl: false,
  });
  geocoder = new google.maps.Geocoder();

  const inputText = document.createElement("input");

  inputText.type = "text";
  inputText.placeholder = "Enter a location";

  const submitButton = document.createElement("input");

  submitButton.type = "button";
  submitButton.value = "Search";
  submitButton.classList.add("button", "button-primary");

  const clearButton = document.createElement("input");

  clearButton.type = "button";
  clearButton.value = "Clear";
  clearButton.classList.add("button", "button-secondary");
  response = document.createElement("pre");
  response.id = "response";
  response.innerText = "";
  responseDiv = document.createElement("div");
  responseDiv.id = "response-container";
  responseDiv.appendChild(response);

  const instructionsElement = document.createElement("p");

  instructionsElement.id = "instructions";
  instructionsElement.innerHTML =
    "<strong>Instructions</strong>: Enter an address to see the movie locations.";
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(inputText);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(submitButton);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(clearButton);
  map.controls[google.maps.ControlPosition.LEFT_TOP].push(instructionsElement);
  map.controls[google.maps.ControlPosition.LEFT_TOP].push(responseDiv);
  marker = new google.maps.Marker({
    map,
  });

  submitButton.addEventListener("click", () =>
    geocode({ address: inputText.value })
  );

  inputText.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      $(submitButton).click();
    }
  });

  clearButton.addEventListener("click", () => {
    clear();
  });
  clear();
}

function clear() {
  marker.setMap(null);
  responseDiv.style.display = "none";
}

function geocode(request) {
  clear();
  geocoder
    .geocode(request)
    .then((result) => {
      const { results } = result;
      map.setCenter(results[0].geometry.location);
      // marker.setPosition(results[0].geometry.location);
      // marker.setMap(map);
      responseDiv.style.display = "hidden";
      response.innerText = JSON.stringify(result, null, 2);

      let lat = JSON.parse(response.innerText).results[0].geometry.location.lat;

      let lng = JSON.parse(response.innerText).results[0].geometry.location.lng;

      // Getting posts based on entered location
      get_posts(lat, lng);

      return results;
    })
    .catch((e) => {
      alert("Geocode was not successful for the following reason: " + e);
    });
}

window.initMap = initMap;

async function get_posts(lat, lng) {
  const resp1 = await axios({
    method: "GET",
    url: "/api/get_locations",
    params: {
      lat: lat,
      lng: lng,
    },
  });

  let resp = resp1.data;

  let movieList = document.getElementById("messages");
  movieList.innerHTML = "";

  // For each post, add marker, add infowindow, add it to the movieList div.
  console.log(resp.posts);
  if (resp.posts.length > 0) {
    resp.posts.forEach((s) => {
      //set marker information
      const infowindow = new google.maps.InfoWindow({
        content: `
       
          <div class="card">
            <a href="/posts/${s.id}">
            <div class="p-3">
            <img class="card-img-top" style="max-height:100px" src="${s.image_url}" alt="Card image cap">
            </div>
            <div class="card-body text-center">
              <h5 class="card-title ">${s.title}</h5>
            </div>
            </a> 
          </div>
        `,
      });

      // The marker, positioned at post locations.
      const marker = new google.maps.Marker({
        position: { lat: s.lat, lng: s.lng },
        map: map,
        title: s.title,
        icon: "/static/images/movie_locations2.png",
      });

      marker.addListener("click", () => {
        infowindow.open({
          anchor: marker,
          map,
          shouldFocus: false,
        });
      });

      google.maps.event.addListener(map, "click", function (event) {
        infowindow.close();
        //autoCenter();
      });

      //create new Div for each post in map and add it to movie-list div.
      let newDiv = document.createElement("div");

      newDiv.innerHTML = `
      <div class="justify-content-center my-1">
        <div class="card p-2 postCard">
          <a href="/posts/${s.id}" class="message-link"></a>
          <image
            class="card-img-top rounded border-0"
            src="${s.image_url}"
          ></image>

          <div class="card-body">
            <h5 class="card-title">${s.title}</h5>
          </div>
          <div class="card-body">
            <p class="my-1">
              <span class="text-muted"><em>Movie:</em></span>
              <span
                ><a href="/movies/{{post.movie.id}}"
                  >${s.movie_title}</a
                ></span>
            </p>
            <p>
              <span class="text-muted"><em>Location:</em></span>
              <span>${s.address}</span>
            </p>
          </div>
        </div>
      </div>
      `;
      movieList.appendChild(newDiv);
    });
  } else {
    movieList.innerHTML = `<h4 class="text-center text-light p-3">Sorry! <br> We currently have no movie location for the location you searched! <br> Please try other locations.</h4>`;
  }
}
