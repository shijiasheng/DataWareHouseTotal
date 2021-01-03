package com.tongji.controller;

import com.tongji.common.api.CommonResult;
import com.tongji.common.exception.Asserts;
import com.tongji.dto.SearchInfo;
import com.tongji.model.Movie;
import com.tongji.service.MovieService;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.*;
import java.util.Map.Entry;

@Controller
@Api(
        tags = {"MovieController"},
        description = "分布式数据库相关API"
)
@RequestMapping({"/distributed"})
public class MovieController {
    @Autowired
    private MovieService movieService;

    public MovieController() {
    }

    @ApiOperation("复杂的条件查询及查询时间统计(查询电影)")
    @RequestMapping(
            value = {"/searchMovie"},
            method = {RequestMethod.POST}
    )
    @ResponseBody
    public CommonResult<Map<String, Object>> searchMovie(@RequestBody Map<String, String> map) {
        try {
            long start = System.currentTimeMillis();
            Integer pageNum = Integer.parseInt((String) map.getOrDefault("pageNum", "1"));
            if (pageNum <= 0) {
                pageNum = 1;
            }

            Integer pageSize = Integer.parseInt((String) map.getOrDefault("pageSize", "5"));
            Integer year = -2;

            try {
                year = Integer.parseInt((String) map.getOrDefault("year", "-2"));
            }
            catch (Exception var28) {
            }

            Integer month = -2;

            try {
                month = Integer.parseInt((String) map.getOrDefault("month", "-2"));
            }
            catch (Exception e) {
            }

            Integer day = -2;

            try {
                day = Integer.parseInt((String) map.getOrDefault("day", "-2"));
            }
            catch (Exception e) {
            }

            Integer quarter = -1;

            try {
                quarter = Integer.parseInt((String) map.getOrDefault("quarter", "-1"));
            }
            catch (Exception e) {
            }

            LinkedList quarterList;
            quarterList = new LinkedList();
            int i;
            label98:
            switch (quarter) {
                case -1:
                    for (i = 1; i <= 12; ++i) {
                        quarterList.add(i);
                    }

                    quarterList.add(-1);
                    break;
                case 0:
                default:
                    Asserts.fail("季度输入有误");
                    break;
                case 1:
                    i = 3;

                    while (true) {
                        if (i > 5) {
                            break label98;
                        }

                        quarterList.add(i);
                        ++i;
                    }
                case 2:
                    i = 6;

                    while (true) {
                        if (i > 8) {
                            break label98;
                        }

                        quarterList.add(i);
                        ++i;
                    }
                case 3:
                    i = 9;

                    while (true) {
                        if (i > 11) {
                            break label98;
                        }

                        quarterList.add(i);
                        ++i;
                    }
                case 4:
                    quarterList.add(12);
                    quarterList.add(1);
                    quarterList.add(2);
            }

            Integer week = -2;

            try {
                Integer.parseInt((String) map.getOrDefault("week", "-2"));
            }
            catch (Exception e) {
            }

            String title = (String) map.get("title");
            String director = (String) map.get("director");
            String actor = (String) map.get("actor");
            boolean isStarring = Boolean.parseBoolean((String) map.getOrDefault("isStarring", "true"));
            String genre = (String) map.get("genre");
            Double score = 0.0D;

            try {
                Double.parseDouble((String) map.getOrDefault("score", "0"));
            }
            catch (Exception e) {
            }

            boolean hasPositive = Boolean.parseBoolean((String) map.getOrDefault("hasPositive", "false"));
            SearchInfo searchInfo = new SearchInfo(pageNum, pageSize, year, month, day, quarterList, week, title, director, actor, isStarring, genre, score, hasPositive);
            Map<String, Object> result = this.movieService.searchMovie(searchInfo);
            long end = System.currentTimeMillis();
            result.put("time", end - start);
            return CommonResult.success(result);
        }
        catch (Exception e) {
            return CommonResult.failed("输入的参数格式有误!");
        }
    }

    @ApiOperation("获取电影详情")
    @RequestMapping(
            value = {"/movie/{id}"},
            method = {RequestMethod.POST}
    )
    @ResponseBody
    public CommonResult<Map<String, Object>> detail(@PathVariable Integer id) {
        long start = System.currentTimeMillis();
        Movie movie = this.movieService.detail(id);
        if (movie == null) {
            return CommonResult.failed("要查询的movie_id不存在!");
        }
        else {
            if (movie.getTitle().equals("##")) {
                movie.setTitle("");
            }

            if (movie.getDirector().equals("##")) {
                movie.setDirector("");
            }

            if (movie.getGenres().equals("##")) {
                movie.setGenres("");
            }

            if (movie.getActor().equals("##")) {
                movie.setActor("");
            }

            if (movie.getSupportingActors().equals("##")) {
                movie.setSupportingActors("");
            }

            Map<String, Object> result = new HashMap();
            if (movie.getLinkId().equals("##")) {
                result.put("linkId", "");
                result.put("linkTitle", "");
                movie.setLinkTitle("");
                movie.setLinkId("");
            }
            else {
                result.put("linkId", movie.getLinkId().replace("$$", ","));
                result.put("linkTitle", movie.getLinkTitle().replace("$$", ","));
            }

            movie.setSupportingActors(movie.getSupportingActors().replace("$$", ","));
            movie.setActor(movie.getActor().replace("$$", ","));
            movie.setGenres(movie.getGenres().replace("$$", ","));
            movie.setDirector(movie.getDirector().replace("$$", ","));
            movie.setLinkTitle(movie.getLinkTitle().replace("$$", ","));
            movie.setLinkId(movie.getLinkId().replace("$$", ","));
            result.put("movie", movie);
            long end = System.currentTimeMillis();
            result.put("time", end - start);
            return CommonResult.success(result);
        }
    }

    @ApiOperation("输入演员，返回导演，合作次数")
    @RequestMapping(
            value = {"/actorToDirector"},
            method = {RequestMethod.POST}
    )
    @ResponseBody
    public CommonResult<Map<String, Object>> actorToDirector(@RequestBody Map<String, String> map) {
        long start = System.currentTimeMillis();
        String actorName = (String) map.get("actorName");
        Map<String, Object> result = new HashMap();
        Map<String, Integer> collaborate = this.movieService.actorToDirector(actorName);
        result.put("total", collaborate.size());
        Integer pageNum = Integer.parseInt((String) map.getOrDefault("pageNum", "1"));
        if (pageNum <= 0) {
            pageNum = 1;
        }

        Integer pageSize = Integer.parseInt((String) map.getOrDefault("pageSize", "10"));
        result.put("pageNum", pageNum);
        result.put("pageSize", pageSize);
        List<Entry<String, Integer>> list = new ArrayList(collaborate.entrySet());
        list.sort(new Comparator<Entry<String, Integer>>() {
            public int compare(Entry<String, Integer> o1, Entry<String, Integer> o2) {
                return ((Integer) o2.getValue()).compareTo((Integer) o1.getValue());
            }
        });
        System.out.println(list);

        while (list.size() > pageSize) {
            list.remove(list.size() - 1);
        }

        result.put("collaborate", list);
        long end = System.currentTimeMillis();
        result.put("time", end - start);
        return CommonResult.success(result);
    }

    @ApiOperation("输入导演，返回演员，合作次数")
    @RequestMapping(
            value = {"/directorToActor"},
            method = {RequestMethod.POST}
    )
    @ResponseBody
    public CommonResult<Map<String, Object>> directorToActor(@RequestBody Map<String, String> map) {
        long start = System.currentTimeMillis();
        String directorName = (String) map.get("directorName");
        Map<String, Object> result = new HashMap();
        Map<String, Integer> collaborate = this.movieService.directorToActor(directorName);
        result.put("total", collaborate.size());
        Integer pageNum = Integer.parseInt((String) map.getOrDefault("pageNum", "1"));
        if (pageNum <= 0) {
            pageNum = 1;
        }

        Integer pageSize = Integer.parseInt((String) map.getOrDefault("pageSize", "10"));
        result.put("pageNum", pageNum);
        result.put("pageSize", pageSize);
        List<Entry<String, Integer>> list = new ArrayList(collaborate.entrySet());
        list.sort(new Comparator<Entry<String, Integer>>() {
            public int compare(Entry<String, Integer> o1, Entry<String, Integer> o2) {
                return ((Integer) o2.getValue()).compareTo((Integer) o1.getValue());
            }
        });
        System.out.println(list);

        while (list.size() > pageSize) {
            list.remove(list.size() - 1);
        }

        result.put("collaborate", list);
        long end = System.currentTimeMillis();
        result.put("time", end - start);
        return CommonResult.success(result);
    }

    @ApiOperation("输入演员，返回演员，合作次数")
    @RequestMapping(
            value = {"/actorToActor"},
            method = {RequestMethod.POST}
    )
    @ResponseBody
    public CommonResult<Map<String, Object>> actorToActor(@RequestBody Map<String, String> map) {
        long start = System.currentTimeMillis();
        String actorName = (String) map.get("actorName");
        Map<String, Object> result = new HashMap();
        Map<String, Integer> collaborate = this.movieService.actorToActor(actorName);
        result.put("total", collaborate.size());
        Integer pageNum = Integer.parseInt((String) map.getOrDefault("pageNum", "1"));
        if (pageNum <= 0) {
            pageNum = 1;
        }

        Integer pageSize = Integer.parseInt((String) map.getOrDefault("pageSize", "10"));
        result.put("pageNum", pageNum);
        result.put("pageSize", pageSize);
        List<Entry<String, Integer>> list = new ArrayList(collaborate.entrySet());
        list.sort(new Comparator<Entry<String, Integer>>() {
            public int compare(Entry<String, Integer> o1, Entry<String, Integer> o2) {
                return ((Integer) o2.getValue()).compareTo((Integer) o1.getValue());
            }
        });
        System.out.println(list);

        while (list.size() > pageSize) {
            list.remove(list.size() - 1);
        }

        result.put("collaborate", list);
        long end = System.currentTimeMillis();
        result.put("time", end - start);
        return CommonResult.success(result);
    }

    @ApiOperation("获取电影评价")
    @RequestMapping(
            value = {"/reviews"},
            method = {RequestMethod.POST}
    )
    @ResponseBody
    public CommonResult<Map<String, Object>> getReview(@RequestBody Map<String, String> map) {
        long start = System.currentTimeMillis();
        Integer pageNum = Integer.parseInt((String) map.getOrDefault("pageNum", "1"));
        if (pageNum <= 0) {
            pageNum = 1;
        }

        Integer pageSize = Integer.parseInt((String) map.getOrDefault("pageSize", "10"));
        Integer movieId = Integer.parseInt((String) map.get("movieId"));
        Map<String, Object> result = new HashMap();
        List<Map<String, Object>> reviews = this.movieService.getReview(movieId);
        int goodCount = 0;
        int badCount = 0;
        int neutralityCount = 0;
        for (Map<String, Object> review : reviews) {
            String tendency = (String) review.get("tendency");
            if (tendency.equals("好评")) {
                ++goodCount;
            }
            else if (tendency.equals("差评")) {
                ++badCount;
            }
            else {
                ++neutralityCount;
            }
        }

        result.put("total", reviews.size());
        result.put("pageNum", pageNum);
        result.put("pageSize", pageSize);
        result.put("goodCount", goodCount);
        result.put("neutralityCount", neutralityCount);
        result.put("badCount", badCount);

        try {
            Random random = new Random();

            while (reviews.size() > pageSize) {
                reviews.remove(random.nextInt(reviews.size()));
            }
        }
        catch (Exception e) {
        }

        result.put("reviews", reviews);
        long end = System.currentTimeMillis();
        result.put("time", end - start);
        return CommonResult.success(result);
    }

    @ApiOperation("获取电影评价图表")
    @RequestMapping(
            value = {"/reviewGraph"},
            method = {RequestMethod.POST}
    )
    @ResponseBody
    public CommonResult<List<Integer>> getReview() {
        List<Integer> result = this.movieService.getReviewGraph();
        return CommonResult.success(result);
    }
}
