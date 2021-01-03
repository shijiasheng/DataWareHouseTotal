package backend.service.neo4j;

import common.*;

import java.util.List;
import java.util.Map;


public interface MovieService
{

    List<ReturnMovieResult> getMovieByDirector(String director);

    int getMovieCount(SearchCommand searchCommand);

    List<ReturnMovieResult> getMovie(SearchCommand searchCommand);

    List<ReturnDirectorResult> getDirectorByActor(String actor, int skip, int limit);

    int getDirectorByActorCount(String actor);

    List<ReturnActorResult> getActorByDirector(String director, int skip, int limit);

    int getActorByDirectorCount(String director);

    List<ReturnActorResult> getActorByActor(String actor,int skip,int limit);

    int getActorByActorCount(String actor);

//    ReturnDTO getMovieByProductId(String id);


    DetailMovieResult getDetailMovie(String product_id);

    List<ReturnReviewResult> getReview(String productId);

    List<ReturnReviewResult> getSeriesReview(String productId);

    Integer getMonthStatistics(String month);

    Integer getWeekStatistics(String toString);
}
