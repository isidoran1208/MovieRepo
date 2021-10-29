import { HttpClient } from "@angular/common/http";
import { Component } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { CommentReaction } from "../model/comment-reaction.model";
import { CommentGet, CommentPost } from "../model/comment.model";
import { Movie } from "../model/movie.model";
import { Reaction } from "../model/reaction.model";

@Component({
  selector: 'app-movie-item',
  templateUrl: './movie-item.component.html',
  styleUrls: ['./movie-item.component.css']
})
export class MovieItemComponent{
  movie: Movie;
  newComment: CommentPost = new CommentPost();

  constructor(private http: HttpClient, private route: ActivatedRoute, private router: Router) {}
  
  ngOnInit(){
    this.getMovie();

    this.newComment.user = parseInt(localStorage.getItem("user_id"));
    this.newComment.movie = this.route.snapshot.params['id'];
  }

  getMovie() {
    this.http.get("http://127.0.0.1:8000/movies/"+this.route.snapshot.params['id']+"/")
    .subscribe((movie: any) => {
      this.movie = movie;
      console.log(this.movie)
    });
  }

  getMovieLikes() {
    return this.movie.reactions.filter(r=>r.reaction==true).length;
  }

  getMovieDislikes() {
    return this.movie.reactions.filter(r=>r.reaction==false).length;
  }

  getCommLikes(comm: CommentGet) {
    return comm.reactions.filter(r=>r.reaction==true).length;
  }

  getCommDislikes(comm: CommentGet) {
    return comm.reactions.filter(r=>r.reaction==false).length;
  }

  onMovieReaction(like: boolean) {
    let reaction = new Reaction(like, parseInt(localStorage.getItem('user_id')), this.movie.id);
    this.http.post("http://127.0.0.1:8000/movies/"+this.route.snapshot.params['id']+"/reactions/", reaction)
    .subscribe((res: Reaction) => {
      this.getMovie();
    });
  }

  movieList() {
    this.router.navigate(["/movies"]);
  }

  onCommentPost() {
    this.http.post("http://127.0.0.1:8000/comments/", this.newComment)
    .subscribe(res => {
      //this.movie.comments.push(res);
      this.getMovie();
      this.newComment.text="";
    });
  }

  onCommentReaction(like: boolean, id: number) {
    let reaction = new CommentReaction(like, parseInt(localStorage.getItem('user_id')), id);
    this.http.post("http://127.0.0.1:8000/comments/"+id+"/reactions/", reaction)
    .subscribe(res => {
      this.getMovie();
    });
  }

  // getLikesDislikes() {
  //   this.http.get("http://127.0.0.1:8000/movies/"+this.route.snapshot.params['id']+"/likes/")
  //   .subscribe((likes: any) => {
  //     this.likes = likes;
  //   });
    
  //   this.http.get("http://127.0.0.1:8000/movies/"+this.route.snapshot.params['id']+"/dislikes/")
  //   .subscribe((dislikes: any) => {
  //     this.dislikes = dislikes;
  //   });
  // }
}