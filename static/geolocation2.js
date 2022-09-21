//GOOGLE MAPS API

let map;
let marker;
let geocoder;
let responseDiv;
let response;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 8,
    center: { lat: 37.7749295, lng: -122.4194155 },
    mapTypeControl: false,
  });
  geocoder = new google.maps.Geocoder();

  const inputText = document.createElement("input");

  inputText.type = "text";
  inputText.placeholder = "Enter a location";

  const submitButton = document.createElement("input");

  submitButton.type = "button";
  submitButton.value = "Submit";
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

  // map.addListener("click", (e) => {
  //   geocode({ location: e.latLng });
  // });

  submitButton.addEventListener("click", () =>
    geocode({ address: inputText.value })
  );

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
      marker.setPosition(results[0].geometry.location);
      marker.setMap(map);
      responseDiv.style.display = "hidden";
      response.innerText = JSON.stringify(result, null, 2);

      console.log(JSON.parse(response.innerText).results);

      let lat = JSON.parse(response.innerText).results[0].geometry.location.lat;

      let lng = JSON.parse(response.innerText).results[0].geometry.location.lng;

      // const resp = await axios({
      //     method: "GET",
      //     url: "/api/get_locations",
      //     params: {
      //       lat: lat,
      //       lng: lng
      //     },
      //   });

      let resp = {
        posts: [
          {
            city: "Sunnyvale",
            created_at: "Mon, 19 Sep 2022 05:06:07 GMT",
            descripton: "dasdas",
            id: 6,
            image_url: "https://pbs.twimg.com/media/En2Kv9KXYAAYLdi.jpg",
            lat: 37.3807069,
            lng: -122.0279504,
            location_id: 6,
            movie_id: 121,
            movie_title: "The Lord of the Rings: The Two Towers",
            state: "CA",
            title: "dsada",
            user_id: 7,
          },
          {
            city: "Sunnyvale",
            created_at: "Mon, 19 Sep 2022 07:31:41 GMT",
            descripton: "asadada",
            id: 7,
            image_url:
              "https://static.wikia.nocookie.net/valley-of-the-wolves/images/e/ed/Polat_Alemdar.jpg/revision/latest/top-crop/width/360/height/360?cb=20210713063128&path-prefix=tr",
            lat: 37.3830028,
            lng: -122.0266886,
            location_id: 7,
            movie_id: 121,
            movie_title: "The Lord of the Rings: The Two Towers",
            state: "CA",
            title: "guzel lokasyon",
            user_id: 7,
          },
        ],
      };

      // results = resp.data.posts;

      let movieList = document.getElementById("messages");
      movieList.innerHTML = "";

      // For each post, add marker, add infowindow, add it to the movieList div.
      resp.posts.forEach((s) => {
        console.log(s);

        //set marker information
        const infowindow = new google.maps.InfoWindow({
          content: `
       
          <div class="card">
            <a href="/posts/${s.id}">
            <img class="card-img-top" src="${s.image_url}" alt="Card image cap">
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
        });

        marker.addListener("click", () => {
          infowindow.open({
            anchor: marker,
            map,
            shouldFocus: false,
          });
        });

        //create new Div for each post in map and add it to messages div.
        let newDiv = document.createElement("div");
        console.log("newDiv");
        console.log(newDiv);

        newDiv.innerHTML = `
          <div class="card">
            <a href="/posts/${s.id}">
            <img class="card-img-top" src="${s.image_url}" alt="Card image cap">
            <div class="card-body text-center">
              <h5 class="card-title ">${s.title}</h5>
              <p class="my-1">
                <span class="text-muted"><em>Movie:</em></span>
                <span>${s.movie_title}</span>
              </p>
              <p class="my-1">
                <span>
                  <span class="text-muted"><em>Location:</em></span>
                  <span>${s.city}, ${s.state}</span>
                </span>
              </p>
            </div>
            </a> 
          </div>
      `;
        movieList.appendChild(newDiv);
      });

      return results;
    })
    .catch((e) => {
      alert("Geocode was not successful for the following reason: " + e);
    });
}

window.initMap = initMap;
