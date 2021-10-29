import { CommentGet } from "./comment.model";
import { Reaction } from "./reaction.model";

export class Movie {
    public id: number;
    public title: string;
    public description: string;
    public start_date: Date;
    public genre: string;
    public photo: File;
    public user: number;
    public comments: CommentGet[];
    public reactions: Reaction[];
}