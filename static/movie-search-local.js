// ** processForm: get data from form and make AJAX call to TMDB API. */
imagePath = "https://image.tmdb.org/t/p/w500";

async function processForm2(evt) {
  let movieName = $("#movie-name").val();

  evt.preventDefault();

  const resp = await axios({
    method: "GET",
    url: "/api/get_movies",
    params: {
      movie: movieName,
    },
  });

  results = resp.data.movies;
  handleResponse(results);
}

function makeDelay(ms) {
  var timer = 0;
  return function (callback) {
    clearTimeout(timer);
    timer = setTimeout(callback, ms);
  };
}
var delay = makeDelay(1000);

/** handleResponse: deal with response from TMDB API. */

function handleResponse(results) {
  $movieList = $("#movie-list");
  $movieList.html("");
  if (results.length > 0) {
    for (let i = 0; i < Math.min(results.length, 10); i++) {
      $movieList.append(`
      <div class="col-4 movie-card">
      <a href="/movies/${results[i].id}">
      <div class="card my-2">
      <img class="card-img-top" src="${imagePath}${results[i].poster_path}" alt="Card image cap">
      <div class="card-body">
      <h5 class="card-title">${results[i].title}</h5>
      <p class="card-text"><em>Release Date: ${results[i].release_date}</em></p>
      
      </div> 
      </a> 
      </div>  
      `);
    }
  } else {
    $movieList.html(
      `<h4 class="text-center text-light p-3">Sorry! <br> We currently have no movie location for the movie you searched! <br> Please try other movies or <a href="/posts/movie_search">post a new movie-location</h4>`
    );
  }
}

$("#movie-search-form-2").on("submit", processForm2);
