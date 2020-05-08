import Search from './components/Search/Search';
import Results from './components/Search/Results';
import Details from './components/Details/Details'
import store from './store';
import { Provider } from 'react-redux';
import React from 'react';
import { Route, BrowserRouter } from 'react-router-dom';

function App() {
  return (
    <div>
      <Provider store={store}>
        <BrowserRouter>
          <Route exact path="/" component={Search}/>
          <Route exact path="/results" component={Results}/>
          <Route exact path="/product/:itemid" component={Details} />
        </BrowserRouter>
      </Provider>
    </div>
  );
}

export default App;
