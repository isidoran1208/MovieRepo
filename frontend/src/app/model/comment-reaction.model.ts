export class CommentReaction {
    public reaction: boolean;
    public user: number;
    public comment: number;

    constructor(reaction: boolean, user: number, comment: number){
        this.reaction = reaction;
        this.user = user;
        this.comment = comment;
    }
}