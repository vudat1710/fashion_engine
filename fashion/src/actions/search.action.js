import { GET_SEARCH_RESULT } from './actionTypes';
import axios from 'axios';

let axiosConfig = {
  headers: {
      'Content-Type': 'application/json;charset=UTF-8',
      "Access-Control-Allow-Origin": "*",
  }
};

export const getSearchResult = (searchParams) => async dispatch => {
    let res;
    if (searchParams["searchType"] === "text") {
        res = await axios.post(`http://0.0.0.0:5000/api/searchText`, searchParams);
    } else {
        console.log(searchParams)
        res = await axios.post(`http://0.0.0.0:5000/api/searchImage`, searchParams, axiosConfig);
    }
    dispatch({
        type: GET_SEARCH_RESULT,
        payload: {
            searchResults: res.data,
            searchParams: searchParams
        }
    })
}
