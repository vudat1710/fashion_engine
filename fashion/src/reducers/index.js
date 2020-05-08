import { combineReducers } from 'redux';
import searchReducer from './search.reducer';

export default combineReducers({
  result: searchReducer
});
