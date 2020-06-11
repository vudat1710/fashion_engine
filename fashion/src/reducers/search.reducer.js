import { GET_SEARCH_RESULT, GET_ERRORS } from '../actions/actionTypes';

const initState = {
    error: '',
    searchData: [],
    isChange: false,
    searchParams: {},
    searchType: "text"
};

export default (state = initState, {type, payload}) => {
    switch (type) {
        case GET_SEARCH_RESULT:
            return {
                ...state,
                searchData: payload.searchResults.response,
                searchParams: payload.searchParams,
                isChange: true,
                searchType: payload.searchResults.searchType
            };
        case GET_ERRORS:
            return {
                ...state,
                error: payload
            };
        default: 
            return state;
    }
};