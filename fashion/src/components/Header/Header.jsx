import React, { Component } from 'react';
import './Header.css';
import { getSearchResult } from '../../actions/search.action'
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import BaseImage from '../../image/is-the-palmer-report-fake-news-6.png';


class Header extends Component {
    constructor(props) {
        super(props);
        this.state = {
            inputSearch: '',
            searchType: "text",
            inputImage: '',
            numResults: 10
        }
    }

    async componentDidMount() {
        const { inputSearch, searchType, inputImage, numResults } = this.props.result.searchParams;
        this.setState({
            ...this.state,
            inputSearch: inputSearch,
            searchType: searchType,
            inputImage: inputImage,
            numResults: numResults
        })
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
        const { searchData } = this.props;
        searchData && searchData();
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

            <div className="container ">
                <br />
                <div className="row d-flex justify-content-center">
                    <div className="col-lg-3 col-md-2 col-sm-12 d-flex align-items-center">
                        <img src={BaseImage} className="header-image img-fluid" alt="google img"></img>
                    </div>
                    <div className="col-lg-9 col-md-8 col-sm-12">
                        {searchBar}
                    </div>
                </div>

                <div className="row">
                    <div className="col-lg-6 col-md-6 col-sm-12">
                        <div className="row d-flex justify-content-center">
                            <div className="col-auto d-flex align-items-center">
                                <h5 style={{ fontWeight: 500 }}>Search Type:</h5>
                            </div>
                            <div className="col-auto">
                                <button className="btn" type="submit" value="text" name="searchType" onClick={(e) => { this.onChange(e) }}>Text</button>
                            </div>
                            <div className="col-auto">
                                <button className="btn" type="submit" value="image" name="searchType" onClick={(e) => { this.onChange(e) }}>Image</button>
                            </div>
                        </div>
                    </div>
                    <div className="small-resize"></div>
                    <div className="col-lg-6 col-md-6 col-sm-12">
                        <div className="row d-flex justify-content-center">
                            <div className="col-auto d-flex align-items-center">
                                <h5 style={{ fontWeight: 500 }}>Num Results:</h5>
                            </div>
                            <div className="col-auto">
                                <select className="btn btn-lg btn-info" name="numResults" onChange={e => this.onChange(e)}>
                                    <option value="10">10</option>
                                    <option value="20">20</option>
                                    <option value="30">30</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            // </div>
        );
    };
}


Header.propTypes = {
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
)(Header);
