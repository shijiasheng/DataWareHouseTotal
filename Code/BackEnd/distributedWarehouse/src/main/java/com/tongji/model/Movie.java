package com.tongji.model;

import io.swagger.annotations.ApiModelProperty;
import java.io.Serializable;

public class Movie implements Serializable {
    private String movieId;
    private String productId;
    private String timeId;
    private String runTime;
    @ApiModelProperty("发布日期")
    private String releaseDate;
    private String dateFirstAvailable;
    @ApiModelProperty("评分")
    private String star;
    private String title;
    private String genres;
    private String director;
    private String supportingActors;
    private String actor;
    private String linkId;
    private String linkTitle;
    private static final long serialVersionUID = 1L;

    public Movie() {
    }

    public String getMovieId() {
        return this.movieId;
    }

    public void setMovieId(String movieId) {
        this.movieId = movieId;
    }

    public String getProductId() {
        return this.productId;
    }

    public void setProductId(String productId) {
        this.productId = productId;
    }

    public String getTimeId() {
        return this.timeId;
    }

    public void setTimeId(String timeId) {
        this.timeId = timeId;
    }

    public String getRunTime() {
        return this.runTime;
    }

    public void setRunTime(String runTime) {
        this.runTime = runTime;
    }

    public String getReleaseDate() {
        return this.releaseDate;
    }

    public void setReleaseDate(String releaseDate) {
        this.releaseDate = releaseDate;
    }

    public String getDateFirstAvailable() {
        return this.dateFirstAvailable;
    }

    public void setDateFirstAvailable(String dateFirstAvailable) {
        this.dateFirstAvailable = dateFirstAvailable;
    }

    public String getStar() {
        return this.star;
    }

    public void setStar(String star) {
        this.star = star;
    }

    public String getTitle() {
        return this.title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getGenres() {
        return this.genres;
    }

    public void setGenres(String genres) {
        this.genres = genres;
    }

    public String getDirector() {
        return this.director;
    }

    public void setDirector(String director) {
        this.director = director;
    }

    public String getSupportingActors() {
        return this.supportingActors;
    }

    public void setSupportingActors(String supportingActors) {
        this.supportingActors = supportingActors;
    }

    public String getActor() {
        return this.actor;
    }

    public void setActor(String actor) {
        this.actor = actor;
    }

    public String getLinkId() {
        return this.linkId;
    }

    public void setLinkId(String linkId) {
        this.linkId = linkId;
    }

    public String getLinkTitle() {
        return this.linkTitle;
    }

    public void setLinkTitle(String linkTitle) {
        this.linkTitle = linkTitle;
    }

    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(this.getClass().getSimpleName());
        sb.append(" [");
        sb.append("Hash = ").append(this.hashCode());
        sb.append(", movieId=").append(this.movieId);
        sb.append(", productId=").append(this.productId);
        sb.append(", timeId=").append(this.timeId);
        sb.append(", runTime=").append(this.runTime);
        sb.append(", releaseDate=").append(this.releaseDate);
        sb.append(", dateFirstAvailable=").append(this.dateFirstAvailable);
        sb.append(", star=").append(this.star);
        sb.append(", title=").append(this.title);
        sb.append(", genres=").append(this.genres);
        sb.append(", director=").append(this.director);
        sb.append(", supportingActors=").append(this.supportingActors);
        sb.append(", actor=").append(this.actor);
        sb.append(", linkId=").append(this.linkId);
        sb.append(", linkTitle=").append(this.linkTitle);
        sb.append(", serialVersionUID=").append(1L);
        sb.append("]");
        return sb.toString();
    }
}
