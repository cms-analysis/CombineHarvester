#include "CombineHarvester/CombineTools/interface/Observation.h"
#include <iostream>
#include "boost/format.hpp"
#include "CombineHarvester/CombineTools/interface/Logging.h"

namespace {
auto format_obs(const ch::Observation& val) {
  return boost::format("%-6s %-9s %-6s %-8s %-28s %-3i %-21s %-10.5g %-5i")
  % val.mass()
  % val.analysis()
  % val.era()
  % val.channel()
  % val.bin()
  % val.bin_id()
  % "data_obs"
  % val.rate()
  % (bool(val.shape()) || bool(val.data()));
}
}

namespace ch {

Observation::Observation()
    : Object(),
      rate_(0.0),
      shape_(),
      data_(nullptr) {
    this->set_process("data_obs");
  }

Observation::~Observation() { }

void swap(Observation& first, Observation& second) {
  using std::swap;
  swap(static_cast<Object&>(first), static_cast<Object&>(second));
  swap(first.rate_, second.rate_);
  swap(first.shape_, second.shape_);
  swap(first.data_, second.data_);
}

Observation::Observation(Observation const& other)
    : Object(other),
      rate_(other.rate_),
      data_(other.data_) {
  TH1* h = nullptr;
  if (other.shape_) {
    h = dynamic_cast<TH1*>(other.shape_->Clone());
    h->SetDirectory(0);
  }
  shape_ = std::unique_ptr<TH1>(h);
}

Observation::Observation(Observation&& other)
    : Object(),
      rate_(0.0),
      shape_(),
      data_(nullptr) {
  swap(*this, other);
}

Observation& Observation::operator=(Observation other) {
  swap(*this, other);
  return (*this);
}

void Observation::set_shape(std::unique_ptr<TH1> shape, bool set_rate) {
  // We were given a nullptr - this is fine, and so we're done
  if (!shape) {
    // This will safely release any existing TH1 held by shape_
    shape_ = nullptr;
    return;
  }
  // Otherwise we validate this new hist. First is to check that all bins have
  // +ve values, otherwise the interpretation as a pdf is tricky
  // for (int i = 1; i <= shape->GetNbinsX(); ++i) {
  //   if (shape->GetBinContent(i) < 0.) {
  //     throw std::runtime_error(FNERROR("TH1 has a bin with content < 0"));
  //   }
  // }
  // At this point we can safely move the shape in and take ownership
  shape_ = std::move(shape);
  // Ensure that root will not try and clean this up
  shape_->SetDirectory(0);
  if (set_rate) {
    this->set_rate(shape_->Integral());
  }
  if (shape_->Integral() > 0.) shape_->Scale(1. / shape_->Integral());
}

void Observation::set_shape(TH1 const& shape, bool set_rate) {
  set_shape(std::unique_ptr<TH1>(static_cast<TH1*>(shape.Clone())), set_rate);
}

std::unique_ptr<TH1> Observation::ClonedShape() const {
  if (!shape_) return std::unique_ptr<TH1>();
  std::unique_ptr<TH1> res(static_cast<TH1 *>(shape_->Clone()));
  res->SetDirectory(0);
  return res;
}

std::unique_ptr<TH1> Observation::ClonedScaledShape() const {
  if (!shape_) return std::unique_ptr<TH1>();
  std::unique_ptr<TH1> res(ClonedShape());
  res->Scale(this->rate());
  return res;
}

TH1F Observation::ShapeAsTH1F() const {
  if (!shape_) {
    throw std::runtime_error(
        FNERROR("Observation object does not contain a shape"));
  }
  TH1F res;
  // Need to get the shape as a concrete type (TH1F or TH1D)
  // A nice way to do this is just to use TH1D::Copy into a fresh TH1F
  TH1F const* test_f = dynamic_cast<TH1F const*>(this->shape());
  TH1D const* test_d = dynamic_cast<TH1D const*>(this->shape());
  if (test_f) {
    test_f->Copy(res);
  } else if (test_d) {
    test_d->Copy(res);
  } else {
    throw std::runtime_error(FNERROR("TH1 shape is not a TH1F or a TH1D"));
  }
  return res;
}

TH2F Observation::ShapeAsTH2F() const {
  if (!shape_) {
    throw std::runtime_error(
        FNERROR("Observation object does not contain a shape"));
  }
  TH2F res;
  // Need to get the shape as a concrete type (TH2F or TH2D)
  // A nice way to do this is just to use TH2D::Copy into a fresh TH2F
  TH2F const* test_f = dynamic_cast<TH2F const*>(this->shape());
  TH2D const* test_d = dynamic_cast<TH2D const*>(this->shape());
  if (test_f) {
    test_f->Copy(res);
  } else if (test_d) {
    test_d->Copy(res);
  } else {
    throw std::runtime_error(FNERROR("TH2 shape is not a TH2F or a TH2D"));
  }
  return res;
}

std::ostream& Observation::PrintHeader(std::ostream &out) {
  std::string line =
    (boost::format("%-6s %-9s %-6s %-8s %-28s %-3i %-21s %-10.5g %-5i")
    % "mass" % "analysis" % "era" % "channel" % "bin" % "id" % "process" %
    "rate" % "shape").str();
  std::string div(line.length(), '-');
  out << div << std::endl;
  out << line << std::endl;
  out << div << std::endl;
  return out;
}

std::string Observation::to_string() const {
  return ::format_obs(*this).str();
}

std::ostream& operator<< (std::ostream &out, Observation const& val) {
  out << ::format_obs(val);
  return out;
}
}
