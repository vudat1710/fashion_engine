import React, { Component } from 'react';
import './Results.css';
import { getSearchResult } from '../../actions/search.action'
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import Pagination from '../Pagination/Pagination';
import Header from '../Header/Header';
import { Link } from 'react-router-dom';

class Search extends Component {

    constructor(props) {

        super(props);
        this.pagination = React.createRef();
        this.state = {
            allData: [],
            currentData: [],
            currentPage: null,
            totalPages: null
        }
    }

    componentDidMount() {
        this.setState({
            ...this.state,
            allData: this.props.result.searchData,
        })
    }

    getBase64(file, cb) {
        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function () {
            cb(reader.result)
        };
        reader.onerror = function (error) {
            console.log('Error: ', error);
        };
    }

    searchData = () => {
        this.setState({ allData: this.props.result.searchData }, () => {
            if (this.pagination && this.pagination.current) {
                this.pagination.current.gotoPage(1);
            }
        })
    }

    onPageChanged = data => {
        // await this.props.result.searchData;
        const { allData } = this.state;
        const { currentPage, totalPages, pageLimit } = data;
        const offset = (currentPage - 1) * pageLimit;
        const currentData = allData.slice(offset, offset + pageLimit);

        this.setState({ currentPage, currentData, totalPages });
    }


    render() {
        let { allData, currentData } = this.state;
        let Content = (allData.length === 0) ? (
            <></>
        ) : (currentData.map((data, ) => {
            if (data.platform === "shopee.vn") {
                data.price = Math.round(data.price / 1e8) * 1e3;
                data.price_before_discount = Math.round(data.price_before_discount / 1e8) * 1e3;
            }
            return (
                    <div className="col-lg-3 col-md-4 col-sm-6" key={data.itemid}>
                        <article className="card card--1">
                            <div className="card__img"></div>
                            <Link to={`/product/${data.itemid}`} className="card-link">
                                <div className="card__img--hover" style={{ backgroundImage: "url(" + process.env.PUBLIC_URL + "/images/" + data.platform.split(".")[0] + "/images/" + data.images[0] + ")" }}></div>
                            </Link>
                            <div className="card__info">
                                <h3 className="card__title">{data.name}</h3>
                                <h3 className="card__category">Score: {data.score}</h3>
                                <span className="card__by">trên <a href="#" className="card__author" title="author">{data.platform}</a></span>
                                <div className="_2lBkmX">
                                    <div className="_1w9jLI QbH7Ig U90Nhh">{data.currency}{data.price_before_discount}</div>
                                    <div className="_1w9jLI _37ge-4 _2ZYSiu" styles={{ maxWidth: "calc(100% - 22px)" }}>
                                        <span className="lwZ9D8">{data.currency}</span><span className="_341bF0">{data.price}</span>
                                    </div>
                                </div>
                            </div>
                        </article>
                    </div>
            );
        }))
        const totalData = (allData === null) ? (
            0
        ) : (
                allData.length
            )
        if (totalData === 0) return (
            <>
                <Header searchData={this.searchData} />
                <div style={{ height: 30 }}></div>
                <div className="container">
                    <h6>Kết quả rỗng</h6>
                </div>
            </>
        )
        return (
            <>
                <Header searchData={this.searchData} />
                <div style={{ height: 30 }}></div>

                <div className="container">
                    <div className="product-section">
                        <nav className="stardust-tabs-header-wrapper" styles={{ top: '7.375rem' }}>
                            <div className="stardust-tabs-header">
                                <div className="stardust-tabs-header__tab stardust-tabs-header__tab--active">
                                    <div className="BFqev7 _1Z8VkJ"></div>
                                    <div className="BBcFUz"><h5 style={{ fontWeight: "bold" }}>KẾT QUẢ LIÊN QUAN</h5></div>
                                </div>
                            </div>
                            {/* <i className="stardust-tabs-header__tab-indicator" styles={{display: "none", width: '216px', transform: "translateX(0px)"}}></i> */}
                        </nav>
                    </div>
                    <div style={{ height: 30 }}></div>
                    <div className="row">
                        {Content}
                    </div>
                    <div style={{ height: 30 }}></div>
                    <Pagination ref={this.pagination} totalRecords={totalData} pageLimit={12} pageNeighbours={1} onPageChanged={this.onPageChanged} />
                    <div style={{ height: 50 }}></div>
                </div>
            </>
        );
    };
}


Search.propTypes = {
    getSearchResult: PropTypes.func.isRequired,
    result: PropTypes.object.isRequired,
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
