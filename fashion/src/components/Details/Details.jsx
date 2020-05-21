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
        const data = searchData.find(x => x.itemid[0] === itemid);
        console.log(searchData)
        await this.setState({
            ...this.state,
            price: data.price[0],
            price_before_discount: data.price_before_discount[0],
            description: data.description[0],
            currency: data.currency[0],
            item_rating: data.item_rating[0],
            liked_count: data.liked_count[0],
            name: data.name[0],
            options: JSON.parse(data.options[0].replace(/'/g, "\"")),
            sex: data.sex[0],
            platform: data.platform[0],
            categories: data.categories,
            images: data.images,
            shop_info: data.shop_info,
            post_url: data.post_url[0],
        })
    }

    render() {
        const { price, price_before_discount, description, currency, item_rating, liked_count,
            name, options, sex, platform, categories, images, shop_info, post_url, rating_star } = this.state;

        let shopContent = Object.keys(shop_info).length === 0 ? (
            <></>
        ) : (
                <div className="container-fluid" style={{ background: "rgba(0,0,0,.02)" }}>
                    <div className="wrapper row">
                        <div className="_2S9T8Y">
                            <div className="col-auto">
                                <div className="_3Lybjn d-flex justify-content-center align-items-center">Tên shop:</div>
                            </div>
                            <div className="col-auto">
                                <div className="_3Lybjn d-flex justify-content-center">{shop_info.name[0]}</div>
                            </div>
                            {/* <div className="_1h7HJr d-flex justify-content-center">{shop_info.account.following_count}{' '}người theo dõi</div> */}
                        </div>
                    </div>
                    <br /><br />
                    <div className="wrapper row">
                        <div className="col-6">
                            <div className="_2S9T8Y">
                                <div className="row">
                                    <div className="col-auto">
                                        <div className="_3Lybjn d-flex justify-content-center align-items-center">Đánh giá:</div>
                                    </div>
                                    <div className="col-auto">
                                        <div className="_3Lybjn d-flex justify-content-center align-items-center">{Number((shop_info.rating_star[0]).toFixed(1))}/5 sao</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="col-6">
                            <div className="_2S9T8Y">
                                <div className="row">
                                    <div className="col-auto">
                                        <div className="_3Lybjn d-flex justify-content-center align-items-center">Địa điểm:</div>
                                    </div>
                                    <div className="col-auto">
                                        <div className="_3Lybjn d-flex justify-content-center align-items-center">{shop_info.shop_location[0]}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div style={{ height: 10 }}></div>
                </div>
            )

        let _images = images.map((path, i) => {
            if (i == 0) {
                return (
                    <div className="tab-pane active" id={`pic-${i}`}><img src={process.env.PUBLIC_URL + "/images/" + platform.split(".")[0] + "/images/" + path} /></div>
                )
            }
            else {
                return (
                    <div className="tab-pane" id={`pic-${i}`}><img src={process.env.PUBLIC_URL + "/images/" + platform.split(".")[0] + "/images/" + path} /></div>
                )
            }
        })


        let colors = Object.keys(options).length === 0 ? (
            <></>
        ) : (
                options["Màu sắc"].map((s, ) => {
                    return (
                        <button className="product-variation">{s}</button>
                    )
                })
            )

        let sizes = Object.keys(options).length === 0 ? (
            <></>
        ) : (
                options["Kích thước"].map((s, ) => {
                    return (
                        <button className="product-variation">{s}</button>
                    )
                })
            )

        let miniImages = images.map((path, i) => {
            if (i == 0) {
                return (
                    <li className="active"><a data-target={`#pic-${i}`} data-toggle="tab"><img src={process.env.PUBLIC_URL + "/images/" + platform.split(".")[0] + "/images/" + path} /></a></li>
                )
            }
            else {
                return (
                    <li><a data-target={`#pic-${i}`} data-toggle="tab"><img src={process.env.PUBLIC_URL + "/images/" + platform.split(".")[0] + "/images/" + path} /></a></li>
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
                                            <div className="col-6 d-flex justify-content-center">
                                                <div class="_3_ISdg">{currency}{price_before_discount}</div>
                                            </div>
                                            <div className="col-6 d-flex justify-content-center">
                                                <div class="_3n5NQx">{currency}{price}</div>
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
                                <h5 className="addition">Giới tính:{'     '}
                                    {sex}
                                    {/* </h5>
                                <h5 className="addition">Đánh giá tốt:{'     '}
                                    {shop_info.rating_good}
                                </h5>
                                <h5 className="addition">Đánh giá không tốt:{'     '}
                                    {shop_info.rating_bad} */}
                                </h5>
                                <h5 className="addition2">Platform:{'     '}
                                    {platform}
                                </h5>
                                <div className="action">
                                    <div className="row">
                                        <div className="col-lg-6 col-md-12 col-sm-12">
                                            <a className="add-to-cart btn btn-default" href={post_url}>TRUY CẬP BÀI VIẾT</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div style={{ height: 30 }}></div>
                <div class="kP-bM3">THÔNG TIN SHOP</div>
                {shopContent}
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
