import React, { Component } from 'react';
import './Search.css';
import { getSearchResult } from '../../actions/search.action'
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import BaseImage from '../../image/is-the-palmer-report-fake-news-6.png';

class Search extends Component {
    constructor(props) {
        super(props);
        this.state = {
            inputSearch: '',
            searchType: "text",
            inputImage: '',
            numResults: 10
        }
    }

    onChange = e => {
        if (e.target.name !== "inputImage") {
            if (e.target.name === "numResults") {
                this.setState({
                    ...this.state,
                    [e.target.name]: parseInt(e.target.value)
                })
            }
            else {
                this.setState({
                    ...this.state,
                    [e.target.name]: e.target.value
                })
            }
        }
        else {
            this.setState({
                ...this.state,
                [e.target.name]: e.target.files[0]
            })
        }
    }

    async onSearch(e) {
        e.preventDefault();
        var canvas = document.createElement('canvas'), ctx = canvas.getContext('2d');
        var uri = canvas.toDataURL('image/png'), b64 = uri.replace(/^data:image.+;base64,/, '');
        this.state.inputImage = b64;
        await this.props.getSearchResult(this.state);
        if (this.props.result.isChange) {
            this.props.history.push('/results')
        }
    }

    render() {
        const { inputSearch } = this.state;
        let searchBar = this.state.searchType === "text" ? (
            <div className="card-body row no-gutters align-items-center">
                <div className="col-auto">
                    <i className="fas fa-search h4 text-body"></i>
                </div>
                <div className="col">
                    <input className="form-control form-control-lg form-control-borderless" type="search" placeholder="Search topics or keywords" name="inputSearch" onChange={e => this.onChange(e)} value={inputSearch} />
                </div>
                <div className="col-auto">
                    <button className="btn btn-lg btn-success" type="submit" onClick={(e) => { this.onSearch(e) }}>Search</button>
                </div>
            </div>
        ) : (
                <div className="card-body row no-gutters align-items-center">
                    <div className="col-auto">
                        <i className="fas fa-search h4 text-body"></i>
                    </div>
                    <div className="col">
                        <input className="form-control form-control-lg form-control-borderless" type="file" placeholder="Upload an image to search" name="inputImage" onChange={e => this.onChange(e)} />
                    </div>
                    <div className="col-auto">
                        <button className="btn btn-lg btn-success" type="submit" onClick={(e) => { this.onSearch(e) }}>Search</button>
                    </div>
                </div>
            );
        return (
            <div className="container">
                <div style={{ height: 100 }}></div>
                <div className="row d-flex justify-content-center">
                    <div className="col-12 col-md-10 col-lg-8 d-flex justify-content-center" >
                        <img src={BaseImage} className="img-fluid imgSearch" alt="google img" style={{ height: "90%", width: "40%" }}></img>
                    </div>
                    <div className="col-12 col-md-10 col-lg-8">
                        <div className="row">
                            <div className="col-10">
                                <div className="card card-sm">
                                    {searchBar}
                                </div>
                            </div>
                            <div className="col-2">
                                <select className="btn btn-lg btn-info" name="numResults" onChange={e => this.onChange(e)}>
                                    <option value="10">10</option>
                                    <option value="20">20</option>
                                    <option value="30">30</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div className="col-12 col-md-10 col-lg-8">
                        <div className="row flex justify-content-center">
                            <div className="col-auto">
                                <button className="btn" type="submit" value="text" name="searchType" onClick={(e) => { this.onChange(e) }}>Text</button>
                            </div>
                            <div className="col-auto">
                                <button className="btn" type="submit" value="image" name="searchType" onClick={(e) => { this.onChange(e) }}>Image</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    };
}


Search.propTypes = {
    result: PropTypes.object.isRequired,
    getSearchResult: PropTypes.func.isRequired,
};

const mapStateToProps = state => ({
    result: state.result
});

const mapDispatchToProps = {
    getSearchResult
};

export default connect(
    mapStateToProps,
    mapDispatchToProps,
)(Search);