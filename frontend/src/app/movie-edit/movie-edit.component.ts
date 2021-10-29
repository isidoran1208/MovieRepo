import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Component } from "@angular/core";
import { Movie } from "../model/movie.model";

@Component({
  selector: 'app-movie-edit',
  templateUrl: './movie-edit.component.html',
})
export class MovieEditComponent {
  movie: Movie = new Movie;
  dt: Date;
  genres;

  constructor(private http: HttpClient) {
    this.genres = [
      {
        id: "TR",
        name: "Thriller"
      },
      {
        id: "RO",
        name: "Romantic"
      },
      {
        id: "AC",
        name: "Action"
      },
      {
        id: "HO",
        name: "Horror"
      },
      {
        id: "CR",
        name: "Crime"
      }
    ];
  }


  onPhotoChange(e) {
    const reader = new FileReader();

    if (e.target.files && e.target.files.length) {
      const [file] = e.target.files;
      this.movie.photo = e.target.files[0];
      console.log(this.movie.photo);
    }
  }

  onMovieAdd() {
    this.movie.user = parseInt(localStorage.getItem('user_id'));
    const data = new FormData();
    Object.keys(this.movie).forEach(k => data.append(k, this.movie[k]));
    this.http.post("http://127.0.0.1:8000/movies/", data)
    .subscribe((responseData: any) => {
      alert("New movie successfully added!");
      this.movie = new Movie();
    });
  }
}