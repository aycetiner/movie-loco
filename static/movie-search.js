// ** processForm: get data from form and make AJAX call to our API. */
MovieAPIKey = "6461108259d95817ace0a23e57345c98";
imagePath = "https://image.tmdb.org/t/p/w500";

async function processForm(evt) {
  let movieName = $("#movie-name").val();

  evt.preventDefault();
  console.log(movieName);
  const resp = await axios({
    method: "GET",
    url: `https://api.themoviedb.org/3/search/movie`,
    params: {
      language: "en-US",
      page: 1,
      include_adult: false,
      api_key: MovieAPIKey,
      query: movieName,
    },
  });
  console.log(resp.data.results);
  results = resp.data.results;
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
      <a class='btn btn-sm btn-primary' href='new/${results[i].id}'>Add Post</a>
      </div>  
      </div>  
      `);
  }
}

$("#movie-search-form").on("submit", processForm);
