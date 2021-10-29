import { HttpClient } from "@angular/common/http";
import { Component } from "@angular/core";
import { Movie } from "../model/movie.model";

@Component({
  selector: 'app-movie-list',
  templateUrl: './movie-list.component.html',
})
export class MovieListComponent{
  movies: Movie[];

  constructor(private http: HttpClient) {
    this.getMovies();
  }
  
  ngOnInit(){

  }

  getMovies() {
    this.http.get("http://127.0.0.1:8000/movies/")
    .subscribe((movies: any) => {
      this.movies = movies.results;
    });
  }

  onMovieDelete(id: number) {
    this.http.delete("http://127.0.0.1:8000/movies/"+id+"/")
    .subscribe(res => {
      this.getMovies();
    });
  }
}