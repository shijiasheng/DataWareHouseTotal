package com.tongji.service.impl;

import com.tongji.common.exception.Asserts;
import com.tongji.dto.SearchInfo;
import com.tongji.model.Actor;
import com.tongji.model.Director;
import com.tongji.model.Genre;
import com.tongji.model.Movie;
import com.tongji.model.Review;
import com.tongji.model.Time;
import com.tongji.service.MovieService;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Service;

@Service
public class MovieServiceImpl implements MovieService {
    @Autowired
    JdbcTemplate jdbcTemplate;

    public MovieServiceImpl() {
    }

    public Map<String, Object> searchMovie(SearchInfo searchInfo) {
        StringBuilder timeSql = new StringBuilder("select movie_id\nfrom movie\nwhere time_id in\n( select time_id from time where 1 = 1 ");
        if (searchInfo.getYear() != -2) {
            timeSql.append("and time.year = ").append(searchInfo.getYear());
        }

        if (searchInfo.getMonth() != -2) {
            timeSql.append(" and time.month = ").append(searchInfo.getMonth());
        }

        if (searchInfo.getDay() != -2) {
            timeSql.append(" and time.day = ").append(searchInfo.getDay());
        }

        if (searchInfo.getWeek() != -2) {
            timeSql.append(" and time.week = ").append(searchInfo.getWeek());
        }

        timeSql.append(" and time.month in (");

        for(int i = 0; i < searchInfo.getQuarterList().size(); ++i) {
            timeSql.append(searchInfo.getQuarterList().get(i));
            if (i != searchInfo.getQuarterList().size() - 1) {
                timeSql.append(",");
            }
        }

        timeSql.append("))");
        List<Integer> moviesIdByTime = null;
        List<Integer> moviesIdByGenre = null;
        List<Integer> moviesIdByDirector = null;
        List<Integer> moviesIdByTitle = null;
        List<Integer> moviesIdByActor = null;
        System.out.println(timeSql.toString());
        moviesIdByTime = this.jdbcTemplate.query(timeSql.toString(), new RowMapper<Integer>() {
            public Integer mapRow(ResultSet resultSet, int i) throws SQLException {
                return resultSet.getInt(1);
            }
        });
        String sql;
        if (searchInfo.getTitle() != null && !searchInfo.getTitle().equals("")) {
            sql = "select movie_id from movie where title = ?";
            moviesIdByTitle = this.jdbcTemplate.query(sql, new RowMapper<Integer>() {
                public Integer mapRow(ResultSet resultSet, int i) throws SQLException {
                    return resultSet.getInt(1);
                }
            }, new Object[]{searchInfo.getTitle()});
        }

        if (searchInfo.getDirector() != null && !searchInfo.getDirector().equals("")) {
            sql = "select movie_id\nfrom movie_director\nwhere director_id in (select director.director_id from director where director.name = ?)\n";
            moviesIdByDirector = this.jdbcTemplate.query(sql, new RowMapper<Integer>() {
                public Integer mapRow(ResultSet resultSet, int i) throws SQLException {
                    return resultSet.getInt(1);
                }
            }, new Object[]{searchInfo.getDirector()});
        }

        if (searchInfo.getActor() != null && !searchInfo.getActor().equals("")) {
            sql = "select movie_id\nfrom movie_actor\nwhere actor_id in (select actor_id from actor where actor.name = ?)";
            if (searchInfo.isStarring()) {
                sql = sql + " and is_supporting = 0";
            } else {
                sql = sql + " and is_supporting = 1";
            }

            moviesIdByActor = this.jdbcTemplate.query(sql, new RowMapper<Integer>() {
                public Integer mapRow(ResultSet resultSet, int i) throws SQLException {
                    return resultSet.getInt(1);
                }
            }, new Object[]{searchInfo.getActor()});
        }

        if (searchInfo.getGenre() != null && !searchInfo.getGenre().equals("")) {
            sql = "select movie_id from movie_genre where genre_id in (select genre_id from genre where genre.name = ?)";
            moviesIdByGenre = this.jdbcTemplate.query(sql, new RowMapper<Integer>() {
                public Integer mapRow(ResultSet resultSet, int i) throws SQLException {
                    return resultSet.getInt(1);
                }
            }, new Object[]{searchInfo.getGenre()});
        }

        if (moviesIdByGenre != null) {
            moviesIdByTime.retainAll(moviesIdByGenre);
        }

        if (moviesIdByTitle != null) {
            moviesIdByTime.retainAll(moviesIdByTitle);
        }

        if (moviesIdByActor != null) {
            moviesIdByTime.retainAll(moviesIdByActor);
        }

        if (moviesIdByDirector != null) {
            moviesIdByTime.retainAll(moviesIdByDirector);
        }

        StringBuilder stringBuilder = new StringBuilder("select movie_id,product_id,title,director from movie where star >= ? and movie_id in (");

        for(int i = 0; i < moviesIdByTime.size(); ++i) {
            stringBuilder.append(moviesIdByTime.get(i));
            if (i != moviesIdByTime.size() - 1) {
                stringBuilder.append(",");
            }
        }

        stringBuilder.append(")");
        stringBuilder.append("limit ?");
        Map<String, Object> result = new HashMap();
        Integer count = moviesIdByTime.size();
        List<Movie> movies = this.jdbcTemplate.query(stringBuilder.toString(), new RowMapper<Movie>() {
            public Movie mapRow(ResultSet resultSet, int i) throws SQLException {
                Movie movie = new Movie();
                movie.setMovieId(resultSet.getString("movie_id"));
                movie.setProductId(resultSet.getString("product_id"));
                movie.setTitle(resultSet.getString("title"));
                movie.setDirector(resultSet.getString("director"));
                return movie;
            }
        }, new Object[]{searchInfo.getScore(), searchInfo.getPageSize()});


        for (Movie movie : movies) {
            movie.setDirector(movie.getDirector().replace("$$", ","));
            movie.setTitle(movie.getTitle().replace("##", ""));
        }


        result.put("total", count);
        result.put("movies", movies);
        return result;
    }

    public List<Director> directors(Integer pageNum, Integer pageSize, String name) {
        String sql = "select * from director where name like ? limit ?,?";
        return this.jdbcTemplate.query(sql, new BeanPropertyRowMapper(Director.class), new Object[]{"%" + name + "%", (pageNum - 1) * pageSize, pageSize});
    }

    public List<Actor> actors(Integer pageNum, Integer pageSize, String name) {
        String sql = "select * from actor where name like ? limit ?,?";
        return this.jdbcTemplate.query(sql, new BeanPropertyRowMapper(Actor.class), new Object[]{"%" + name + "%", (pageNum - 1) * pageSize, pageSize});
    }

    public List<Genre> genre(Integer pageNum, Integer pageSize, String name) {
        String sql = "select * from genre where name like ? limit ?,?";
        return this.jdbcTemplate.query(sql, new BeanPropertyRowMapper(Genre.class), new Object[]{"%" + name + "%", (pageNum - 1) * pageSize, pageSize});
    }

    public List<Time> times(Integer pageNum, Integer pageSize, Integer year, Integer month, Integer day, Integer week, List<Integer> quarterList) {
        StringBuilder timeSql = new StringBuilder("select * from time where 1 = 1 ");
        if (year != -2) {
            timeSql.append("and time.year = ").append(year);
        }

        if (month != -2) {
            timeSql.append(" and time.month = ").append(month);
        }

        if (day != -2) {
            timeSql.append(" and time.day = ").append(day);
        }

        if (week != -2) {
            timeSql.append(" and time.week = ").append(week);
        }

        timeSql.append(" and time.month in (");

        for(int i = 0; i < quarterList.size(); ++i) {
            timeSql.append(quarterList.get(i));
            if (i != quarterList.size() - 1) {
                timeSql.append(",");
            }
        }

        timeSql.append(") limit ?,?");
        return this.jdbcTemplate.query(timeSql.toString(), new BeanPropertyRowMapper(Time.class), new Object[]{(pageNum - 1) * pageSize, pageSize});
    }

    public Movie detail(Integer id) {
        String sql = "select * from movie where movie_id = ?";
        return (Movie)this.jdbcTemplate.queryForObject(sql, new RowMapper<Movie>() {
            public Movie mapRow(ResultSet resultSet, int i) throws SQLException {
                Movie movie = new Movie();
                movie.setMovieId(resultSet.getString("movie_id"));
                movie.setProductId(resultSet.getString("product_id"));
                movie.setTimeId(resultSet.getString("time_id"));
                movie.setTitle(resultSet.getString("title"));
                movie.setGenres(resultSet.getString("genres"));
                movie.setDirector(resultSet.getString("director"));
                movie.setSupportingActors(resultSet.getString("supporting_actors"));
                movie.setActor(resultSet.getString("actor"));
                movie.setRunTime(resultSet.getString("run_time"));
                movie.setReleaseDate(resultSet.getString("release_date"));
                movie.setDateFirstAvailable(resultSet.getString("date_first_available"));
                movie.setStar(resultSet.getString("star"));
                movie.setLinkId(resultSet.getString("link_id"));
                movie.setLinkTitle(resultSet.getString("link_title"));
                return movie;
            }
        }, new Object[]{id});
    }

    public List<Map<String, Object>> getReview(Integer movieId) {
        List<String> productIds = new LinkedList();
        Movie movie = this.detail(movieId);
        if (movie == null) {
            Asserts.fail("movieId不存在");
        }

        productIds.add(movie.getProductId());
        String linkId = movie.getLinkId();
        if (!linkId.equals("##")) {
            String[] products = linkId.split("\\$\\$");
            for (String productId : productIds) {
                productIds.add(productId);
            }
        }

        System.out.println(productIds);
        StringBuilder sql = new StringBuilder("select profile_name,score,star from review where product_id in (");

        for(int i = 0; i < productIds.size(); ++i) {
            sql.append("'");
            sql.append((String)productIds.get(i));
            sql.append("'");
            if (i != productIds.size() - 1) {
                sql.append(",");
            }
        }

        sql.append(")");
        System.out.println(sql.toString());
        final List<Map<String, Object>> list = new LinkedList();
        List<Review> query = this.jdbcTemplate.query(sql.toString(), new RowMapper<Review>() {
            public Review mapRow(ResultSet resultSet, int i) throws SQLException {
                Map<String, Object> result = new HashMap();
                result.put("profile_name", resultSet.getString("profile_name"));
                result.put("score", resultSet.getDouble("score"));
                double star = resultSet.getDouble("star");
                if (star < 0.05D) {
                    result.put("tendency", "差评");
                } else if (star > 0.95D) {
                    result.put("tendency", "好评");
                } else {
                    result.put("tendency", "中立");
                }

                list.add(result);
                return null;
            }
        });
        System.out.println(list);
        return list;
    }

    public Map<String, Integer> actorToDirector(String actorName) {
        String sql = "select actor_id from actor where actor.name = ?";
        Integer id = (Integer)this.jdbcTemplate.queryForObject(sql, Integer.class, new Object[]{actorName});
        sql = "select name, count\nfrom director,\n     director_actor\nwhere director.director_id = director_actor.director_id\n  and actor_id = ?";
        final Map<String, Integer> result = new HashMap();
        this.jdbcTemplate.query(sql, new RowMapper<Director>() {
            public Director mapRow(ResultSet resultSet, int i) throws SQLException {
                result.put(resultSet.getString("name"), resultSet.getInt("count"));
                return null;
            }
        }, new Object[]{id});
        return result;
    }

    public Map<String, Integer> directorToActor(String directorName) {
        String sql = "select director_id from director where director.name = ?";
        Integer id = (Integer)this.jdbcTemplate.queryForObject(sql, Integer.class, new Object[]{directorName});
        sql = "select name, count\nfrom actor,\n     director_actor\nwhere actor.actor_id = director_actor.actor_id and director_id = ?";
        final Map<String, Integer> result = new HashMap();
        this.jdbcTemplate.query(sql.toString(), new RowMapper<Director>() {
            public Director mapRow(ResultSet resultSet, int i) throws SQLException {
                result.put(resultSet.getString("name"), resultSet.getInt("count"));
                return null;
            }
        }, new Object[]{id});
        return result;
    }

    public Map<String, Integer> actorToActor(String actorName) {
        String sql = "select actor_id from actor where actor.name = ?";
        Integer id = (Integer)this.jdbcTemplate.queryForObject(sql, Integer.class, new Object[]{actorName});
        sql = "select name, count\nfrom actor,\n     actor_actor\nwhere actor.actor_id = actor_actor.actor_id_2\n  and actor_id_1 = ?";
        System.out.println(sql);
        final Map<String, Integer> result = new HashMap();
        this.jdbcTemplate.query(sql, new RowMapper<Director>() {
            public Director mapRow(ResultSet resultSet, int i) throws SQLException {
                result.put(resultSet.getString("name"), resultSet.getInt("count"));
                return null;
            }
        }, new Object[]{id});
        return result;
    }

    public List<Integer> getReviewGraph() {
        List<Integer> result = new LinkedList();
        final int[] temp = new int[3];
        String sql = "select star from review";
        this.jdbcTemplate.query(sql, new RowMapper<Review>() {
            public Review mapRow(ResultSet resultSet, int i) throws SQLException {
                String test = resultSet.getString("star");
                Double star = 0.5D;

                try {
                    star = Double.parseDouble(test);
                } catch (Exception e) {
                }

                if (star < 0.05D) {
                    temp[2]++;
                } else if (star > 0.95D) {
                    temp[0]++;
                } else {
                    temp[1]++;
                }

                return null;
            }
        });

        for(int i = 0; i < temp.length; ++i) {
            result.add(temp[i]);
        }

        return result;
    }
}
