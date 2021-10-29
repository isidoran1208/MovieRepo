export class Reaction {
    public reaction: boolean;
    public user: number;
    public movie: number;

    constructor(reaction: boolean, user: number, movie: number){
        this.reaction = reaction;
        this.user = user;
        this.movie = movie;
    }
}