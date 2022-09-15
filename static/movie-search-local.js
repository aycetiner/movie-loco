// ** processForm: get data from form and make AJAX call to our API. */
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

/** handleResponse: deal with response from our lucky-num API. */

function handleResponse(results) {
  $movieList = $("#movie-list");
  $movieList.html("");

  for (let i = 0; i < Math.min(results.length, 10); i++) {
    $movieList.append(`
      <div class="col-3">
      <div class="card">
      <img class="card-img-top" src="${imagePath}${results[i].poster_path}" alt="Card image cap">
      <div class="card-body">
      <h5 class="card-title">${results[i].title}</h5>
      <p class="card-text">${results[i].release_date}</p>
      <a class='btn btn-sm btn-primary' href='movies/${results[i].id}'>Go Movie Posts</a>
      </div>  
      </div>  
      `);
  }
}

$("#movie-search-form-2").on("submit", processForm2);
