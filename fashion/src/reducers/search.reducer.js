import { GET_SEARCH_RESULT, GET_ERRORS } from '../actions/actionTypes';

const initState = {
    error: '',
    searchData: [],
    isChange: false,
    searchParams: {}
};

export default (state = initState, {type, payload}) => {
    switch (type) {
        case GET_SEARCH_RESULT:
            return {
                ...state,
                searchData: payload.searchResults,
                searchParams: payload.searchParams,
                isChange: true
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