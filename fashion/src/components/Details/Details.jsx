import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import './Details.css';
import './Star.scss';
import { Link } from 'react-router-dom';

class Details extends Component {
    constructor(props) {
        super(props);
        this.state = {
            price: 0,
            price_before_discount: 0,
            currency: '',
            item_rating: 0,
            liked_count: 0,
            name: '',
            options: {},
            sex: '',
            platform: '',
            categories: [],
            description: '',
            images: [],
            rating_star: 0,
            shop_info: {
            }
        }
    }

    async componentDidMount() {
        const itemid = parseInt(this.props.match.params.itemid);
        const searchData = this.props.result.searchData;
        const data = searchData.find(x => x.itemid === itemid);

        await this.setState({
            ...this.state,
            price: data.price,
            price_before_discount: data.price_before_discount,
            description: data.description,
            currency: data.currency,
            item_rating: data.item_rating,
            liked_count: data.liked_count,
            name: data.name,
            options: JSON.parse(data.options.replace(/'/g, "\"")),
            sex: data.sex,
            platform: data.platform,
            categories: data.categories,
            images: data.images,
            shop_info: data.shop_info,
            post_url: data.post_url,
        })
    }

    render() {
        const { price, price_before_discount, description, currency, item_rating, liked_count,
            name, options, sex, platform, categories, images, shop_info, post_url } = this.state;
        let price_, price_before_discount_, price_before_discount_comp;

        let shop_name = shop_info.name === undefined ? ("") : (shop_info.name);

        if (platform === "shopee.vn") {
            price_ = Math.round(price / 1e8) * 1e3;
            price_before_discount_ = Math.round(price_before_discount / 1e8) * 1e3
        } else {
            price_ = price;
            price_before_discount_ = price_before_discount;
        }

        price_before_discount_comp = (price_ !== price_before_discount_) && (price_before_discount_ !== 0) ? (
            <div className="col-6 d-flex justify-content-center">
                <div class="_3_ISdg">{currency}{price_before_discount_}</div>
            </div>
        ) : (
            <div className="col-6 d-flex justify-content-center">
            </div>
        )

        let _images = images.map((path, i) => {
            if (i === 0) {
                return (
                    <div className="tab-pane active" id={`pic-${i}`}><img src={process.env.PUBLIC_URL + "/images/" + platform.split(".")[0] + "/images/" + path} alt="product"/></div>
                )
            }
            else {
                return (
                    <div className="tab-pane" id={`pic-${i}`}><img src={process.env.PUBLIC_URL + "/images/" + platform.split(".")[0] + "/images/" + path} alt="product"/></div>
                )
            }
        })


        let colors = Object.keys(options).length === 0 ? (
            <></>
        ) : (
                options[Object.keys(options)[0]].map((s, ) => {
                    return (
                        <button className="product-variation">{s}</button>
                    )
                })
            )

        let sizes = Object.keys(options).length === 0 ? (
            <></>
        ) : (
                (Object.keys(options)[1] !== undefined) ? (
                    options[Object.keys(options)[1]].map((s, ) => {
                        return (
                            <button className="product-variation">{s}</button>
                        )
                    })
                ) : (
                        <></>
                    )
            )

        let _categories = categories.map((c, ) => {
            return (
                <button className="product-variation">{c}</button>
            )
        })

        let miniImages = images.map((path, i) => {
            if (i === 0) {
                return (
                    <li className="active"><a data-target={`#pic-${i}`} data-toggle="tab"><img src={process.env.PUBLIC_URL + "/images/" + platform.split(".")[0] + "/images/" + path} alt="product"/></a></li>
                )
            }
            else {
                return (
                    <li><a data-target={`#pic-${i}`} data-toggle="tab"><img src={process.env.PUBLIC_URL + "/images/" + platform.split(".")[0] + "/images/" + path} alt="product"/></a></li>
                )
            }
        })
        return (
            <div className="container">
                <div className="card-details">
                    <div className="container-fluid">
                        <div className="wrapper row">
                            <div className="preview col-md-6">
                                <div className="preview-pic tab-content">
                                    {_images}
                                </div>
                                <ul className="preview-thumbnail nav nav-tabs">
                                    {miniImages}
                                </ul>
                            </div>
                            <div className="details col-md-6">
                                <h3 className="product-title">{name}</h3>
                                <div className="rate">
                                    <div class="star-ratings">
                                        <div class="star-ratings-top" style={{ width: 100 * parseFloat(item_rating) / 4.55 + "%" }}><span>★</span><span>★</span><span>★</span><span>★</span><span>★</span></div>
                                        <div class="star-ratings-bottom"><span>☆</span><span>☆</span><span>☆</span><span>☆</span><span>☆</span></div>
                                    </div>
                                    {/* <span className="review-no">{brand}</span> */}
                                </div>

                                <div className="row">
                                    <div className="col-auto d-flex align-items-center">
                                        <h5 style={{ fontWeight: 500 }}>Giá:</h5>
                                    </div>
                                    <div className="col-auto">
                                        <div className="row">
                                            {price_before_discount_comp}
                                            <div className="col-6 d-flex justify-content-center">
                                                <div class="_3n5NQx">{currency}{price_}</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <h6 className="vote"><strong>{liked_count}</strong> người thích sản phẩm này </h6>
                                <h5 className="sizes">sizes:{'      '}
                                    {sizes}
                                </h5>
                                <h5 className="colors">Màu:{'     '}
                                    {colors}
                                </h5>
                                <h5 className="colors">Loại:{'     '}
                                    {_categories}
                                </h5>
                                <h5 className="addition">Giới tính:{'     '}
                                    {sex}
                                </h5>
                                <h5 className="addition">Tên shop:{'     '}
                                    {shop_name}
                                </h5>
                                <h5 className="addition2">Platform:{'     '}
                                    {platform}
                                </h5>
                                <div className="action">
                                    <div className="row">
                                        <div className="col-lg-6 col-md-12 col-sm-12">
                                            <a className="add-to-cart btn btn-default" target='_blank' href={post_url}>TRUY CẬP BÀI VIẾT</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div style={{ height: 30 }}></div>
                <div class="kP-bM3">MÔ TẢ SẢN PHẨM</div>
                <div className="container-fluid" style={{ background: "rgba(0,0,0,.02)" }}>
                    <div className="wrapper row">
                        <div class="_2aZyWI">
                            <div class="_2u0jt9">
                                <span>{description}</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div style={{ height: 10 }}></div>
                <div className="col-lg-6 col-md-12 col-sm-12">
                    <Link className="add-to-cart btn btn-default" to='/'>TRỞ VỀ TRANG CHỦ</Link>
                </div>
                <div style={{ height: 30 }}></div>
            </div>
        );
    };
}


Details.propTypes = {
    result: PropTypes.object.isRequired,
};

const mapStateToProps = state => ({
    result: state.result
});

const mapDispatchToProps = {
};

export default connect(
    mapStateToProps,
    mapDispatchToProps,
)(Details);
