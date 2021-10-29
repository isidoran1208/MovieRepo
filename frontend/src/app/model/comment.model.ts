import { Reaction } from "./reaction.model";
import { User } from "./user.model";

export class CommentGet {
    public id: number;
    public text: string;
    public user: User;
    public reply_to: number;

    public reactions: Reaction[];
    public replies: CommentGet[];
}

export class CommentPost {
    public text: string;
    public user: number;
    public movie: number;
    public reply_to: number;
}