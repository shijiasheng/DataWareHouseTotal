package backend.service.neo4j.impl;

import backend.dao.neo4j.MovieMapper;
import backend.service.neo4j.MovieService;
import common.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;


import java.util.*;


@Service
public class MovieServiceImpl implements MovieService
{

    @Autowired
    MovieMapper movieMapper;

    @Override
    public DetailMovieResult getDetailMovie(String product_id)
    {
//        System.out.println(product_id);
        DetailMovieResult res = this.movieMapper.getDetailMovie(product_id);
//        System.out.println(res);
        return res;
    }

    @Override
    public List<ReturnReviewResult> getReview(String productId)
    {
//        System.out.println(productId);
        List<ReturnReviewResult> res = this.movieMapper.getReview(productId);
//        System.out.println(res);
        return res;
    }

    @Override
    public List<ReturnReviewResult> getSeriesReview(String productId)
    {
//        System.out.println(productId);
        List<ReturnReviewResult> res = this.movieMapper.getSeriesReview(productId);
//        System.out.println(res);
        return res;
    }

    @Override
    public Integer getMonthStatistics(String month)
    {
        return this.movieMapper.getMonthStatistics(month);
    }

    @Override
    public Integer getWeekStatistics(String week)
    {
        return this.movieMapper.getWeekStatistics(week);
    }

    @Override
    public List<ReturnMovieResult> getMovie(SearchCommand searchCommand)
    {

//        System.out.println(searchCommand);
        List<ReturnMovieResult> res = this.movieMapper.getMovie(searchCommand);
//        System.out.println(res);
        return res;
    }

    @Override
    public List<ReturnDirectorResult> getDirectorByActor(String actor, int skip, int limit)
    {
//        System.out.println(actor);
        List<ReturnDirectorResult> res = this.movieMapper.getDirectorByActor(actor, skip, limit);
//        System.out.println(res);
        return res;
    }

    @Override
    public int getDirectorByActorCount(String actor)
    {
        return this.movieMapper.getDirectorByActorCount(actor);
    }

    @Override
    public List<ReturnActorResult> getActorByDirector(String director, int skip, int limit)
    {
//        System.out.println(director);
        List<ReturnActorResult> res = this.movieMapper.getActorByDirector(director, skip, limit);
//        System.out.println(res);
        return res;
    }

    @Override
    public int getActorByDirectorCount(String director)
    {
        System.out.println(director);
        int res = this.movieMapper.getActorByDirectorCount(director);
        System.out.println(res);
        return res;
    }

    @Override
    public List<ReturnActorResult> getActorByActor(String actor, int skip, int limit)
    {
//        System.out.println(actor);
        List<ReturnActorResult> res = this.movieMapper.getActorByActor(actor, skip, limit);
//        System.out.println(res);
        return res;
    }

    @Override
    public int getActorByActorCount(String actor)
    {
        System.out.println(actor);
        int res = this.movieMapper.getActorByActorCount(actor);
        System.out.println(res);
        return res;
    }

    @Override
    public List<ReturnMovieResult> getMovieByDirector(String director)
    {
        System.out.println(director);
        List<ReturnMovieResult> res = this.movieMapper.getMovieByDirector(director);
        System.out.println(res);
        return res;
    }

    @Override
    public int getMovieCount(SearchCommand searchCommand)
    {
        System.out.println(searchCommand);
        return this.movieMapper.getMovieCount(searchCommand);
    }

}
