package backend.dao.neo4j;

import common.*;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Mapper
@Repository
public interface MovieMapper
{

    DetailMovieResult getDetailMovie(String product_id);

    int getMovieCount(@Param("searchCommand") SearchCommand searchCommand);

    List<ReturnMovieResult> getMovie(@Param("searchCommand") SearchCommand searchCommand);

    List<ReturnDirectorResult> getDirectorByActor(@Param("actor") String actor, @Param("skip") int skip, @Param("limit") int limit);

    List<ReturnActorResult> getActorByDirector(@Param("director") String director, @Param("skip") int skip, @Param("limit") int limit);

    List<ReturnActorResult> getActorByActor(@Param("actor") String actor, @Param("skip") int skip, @Param("limit") int limit);

    List<ReturnMovieResult> getMovieByDirector(String director);

    int getDirectorByActorCount(String actor);

    int getActorByDirectorCount(String director);

    int getActorByActorCount(String actor);

    List<ReturnReviewResult> getReview(@Param("productId") String productId);

    List<ReturnReviewResult> getSeriesReview(@Param("productId") String productId);

    Integer getMonthStatistics(String month);

    Integer getWeekStatistics(String week);
}
